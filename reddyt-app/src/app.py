import os

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_oauth2 import requests
from authlib.jose import JsonWebKey
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .db_service import DBService
from .env_service import EnvService
from .router import Router


# Tell Flask it is Behind a Proxy: https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
def enable_proxy(app):
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    print("Successfully configured nginx reverse proxy in Flask.", flush=True)


application = Flask(__name__)

EnvService.init()
try:
    if EnvService.env.bool("PROXY_EXISTS"):
        enable_proxy(application)
except Exception:
    print("No reverse proxy configured.")
DBService.init()

application.secret_key = EnvService.env.str("APP_SECRET_KEY")
oauth = OAuth(application)
keycloak = oauth.register(
    name="keycloak",
    client_id=EnvService.env("KEYCLOAK_CLIENT_ID"),
    client_secret=EnvService.env("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=EnvService.env("KEYCLOAK_METADATA_URL"),
    client_kwargs={"scope": "openid profile email"},
)

router = Router(application, keycloak)

print("Started Flask app.", flush=True)
