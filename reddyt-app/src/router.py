from flask import render_template, redirect, abort
from flask import request

class Router:
    def __init__(self, app):

        @app.route("/health")
        def health_endpoint():
            return "success", 200

        @app.get("/")
        def index():
            return render_template('index.html')

        @app.get("/create-post")
        def create_post():
            return render_template('pages/create-post.html')
