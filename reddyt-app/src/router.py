from flask import render_template, redirect, abort
from flask import request

class Router:
    def __init__(self, app):

        @app.route("/health")
        def health_endpoint():
            return "success", 200
