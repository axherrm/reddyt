from flask import Flask

app = Flask(__name__)

@app.get("/")
def display_index():
    return """
    <p>Hello World!</p>
    <p><a href="/logout">Logout</a></p>
    """