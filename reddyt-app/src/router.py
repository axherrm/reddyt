import secrets
import sys

from authlib.oauth2 import OAuth2Error
from flask import render_template, redirect, url_for, session
from flask import request

class Router:
    def __init__(self, app, keycloak):
        self.app = app
        self.keycloak = keycloak
        self.init_backend()
        self.init_frontend()

    def init_frontend(self):
        @self.app.before_request
        def check_authentication():
            if request.endpoint in ["login", "callback"]:
                return
            if "user" not in session:
                return redirect(url_for("login"))

        @self.app.get("/")
        def display_index():
            from .model.post import Post
            from .model.user import User
            return render_template('index.html', user=User.get_by_id(session['user']['sub']), posts=Post.select())

        @self.app.get("/posts/<int:post_id>")
        def display_post(post_id):
            from .model.post import Post
            from .model.comment import Comment
            from .model.user import User
            return render_template('pages/post.html', user=User.get_by_id(session['user']['sub']), post=Post.get_by_id(post_id), comments=Comment.select().where(Comment.post == post_id))

        @self.app.get("/create-post")
        def display_create_post():
            from .model.user import User
            return render_template('pages/create-post.html', user=User.get_by_id(session['user']['sub']))

    def init_backend(self):
        @self.app.route("/login")
        def login():
            nonce = secrets.token_urlsafe(16)
            session['nonce'] = nonce
            # from .env_service import EnvService
            redirect_uri = url_for('callback', _external=True) # EnvService.env("REDIRECT_URI")
            return self.keycloak.authorize_redirect(redirect_uri, nonce=nonce)

        @self.app.route("/callback")
        def callback():
            try:
                # TODO: remove
                print(request.args.get('state'), file=sys.stdout)
                print(session, file=sys.stdout)
                sys.stdout.flush()
                token = self.keycloak.authorize_access_token()
                session['token'] = token
                user_info = self.keycloak.parse_id_token(token, session.pop("nonce", None))
                session['user'] = user_info
                from .model.user import User
                User.get_or_create(
                        username=user_info["sub"],
                        email=user_info["email"],
                        last_name=user_info["family_name"],
                        first_name=user_info["given_name"],
                )
                return redirect("/")
            except OAuth2Error as error:
                return f"Authentication failed: {error.description}"

        @self.app.post('/logout')
        def logout():
            id_token = session['token']['id_token']
            if not id_token:
                return redirect(url_for('login'))

            from .env_service import EnvService
            keycloak_logout_url = (
                f"{EnvService.env("KEYCLOAK_METADATA_URL").replace('/.well-known/openid-configuration', '')}/protocol/openid-connect/logout"
            )
            logout_params = {
                'id_token_hint': id_token,
                'post_logout_redirect_uri': url_for('login', _external=True), # EnvService.env("LOGOUT_REDIRECT_URI")
            }
            session.clear()
            return redirect(
                f"{keycloak_logout_url}?id_token_hint={logout_params['id_token_hint']}&post_logout_redirect_uri={logout_params['post_logout_redirect_uri']}")

        @self.app.route("/health")
        def health_endpoint():
            return "success", 200

        @self.app.post("/api/create-post")
        def create_post():
            from .model.post import Post
            new_post = Post.create(
                title=request.form['title'],
                content=request.form['content'],
                user=session['user']['sub']
            )
            return redirect(url_for("display_post", post_id=new_post.id))

        @self.app.post("/api/create-comment")
        def create_comment():
            from .model.comment import Comment
            Comment.create(
                content=request.form['content'],
                post=request.form['post-id'],
                user=session['user']['sub']
            )
            return redirect(url_for("display_post", post_id=request.form['post-id']))
