from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .router import Router

def start(proxy_exists: bool = False):
    app = Flask(__name__)

    if proxy_exists:
        enable_proxy(app)

    router = Router(app)

    print("Started Flask app.", flush=True)
    return app

# Tell Flask it is Behind a Proxy: https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
def enable_proxy(app):
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    print("Successfully configured nginx reverse proxy in Flask.", flush=True)