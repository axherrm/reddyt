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
router = Router(application)

print("Started Flask app.", flush=True)
