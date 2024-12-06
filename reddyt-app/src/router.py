from flask import render_template, redirect, url_for
from flask import request

class Router:
    def __init__(self, app):
        self.app = app
        self.init_backend()
        self.init_frontend()

    def init_frontend(self):
        @self.app.get("/")
        def display_index():
            # from .model.post import Post
            # posts = Post.select()
            # return render_template('index.html', posts=posts)
            return render_template('index.html')

        @self.app.get("/posts/<int:post_id>")
        def display_post(post_id):
            from .model.post import Post
            post = Post.get_by_id(post_id)
            return render_template('pages/post.html', post=post)

        @self.app.get("/create-post")
        def display_create_post():
            return render_template('pages/create-post.html')

    def init_backend(self):
        @self.app.route("/health")
        def health_endpoint():
            return "success", 200

        @self.app.post("/api/create-post")
        def create_post():
            from .model.post import Post
            new_post = Post.create(
                title=request.form['title'],
                content=request.form['content'],
            )
            return redirect(url_for("display_post", post_id=new_post.id))

        @self.app.post("/api/create-comment")
        def create_comment():
            from .model.comment import Comment
            Comment.create(
                content=request.form['content'],
                post=request.form['post-id'],
            )
            return redirect(url_for("display_post", post_id=request.form['post-id']))
