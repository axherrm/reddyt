import secrets

from authlib.integrations.flask_client import OAuth
from authlib.oauth2 import OAuth2Error
from flask import Flask, request, session, url_for, redirect

app = Flask(__name__)

app.secret_key = "<some-very-secret-string>" # Don't do this in production
oauth = OAuth(app)
keycloak = oauth.register(
    name="keycloak",
    client_id="simple-web-app", # Please use environment variables for these in production
    client_secret="lmG9Tx16hrulnvD2YfYsNxNbGd6WSfwC",
    server_metadata_url="http://keycloak:7080/realms/simple-web-application-realm/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

@app.before_request
def check_authentication():
    if request.endpoint in ["login", "callback"]:
        return
    if "user" not in session:
        return redirect(url_for("login"))

@app.get("/")
def display_index():
    return """
    <p>Hello World!</p>
    <p><a href="/logout">Logout</a></p>
    """

@app.route("/login")
def login():
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    redirect_uri = url_for('callback', _external=True)
    return keycloak.authorize_redirect(redirect_uri, nonce=nonce)

@app.route("/callback")
def callback():
    try:
        token = keycloak.authorize_access_token()
        session['token'] = token
        user_info = keycloak.parse_id_token(token, session.pop("nonce", None))
        session['user'] = user_info
        return redirect("/")
    except OAuth2Error as error:
        return f"Authentication failed: {error.description}"

@app.route('/logout')
def logout():
    id_token = session['token']['id_token']
    if not id_token:
        return redirect(url_for('login'))
    keycloak_logout_url = "http://localhost:7080/realms/simple-web-application-realm/protocol/openid-connect/logout"
    post_logout_redirect_uri = url_for('login', _external=True)
    session.clear()
    return redirect(
        f"{keycloak_logout_url}?id_token_hint={id_token}&post_logout_redirect_uri={post_logout_redirect_uri}")
