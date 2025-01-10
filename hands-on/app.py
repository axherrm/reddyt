from flask import Flask

app = Flask(__name__)

@app.get("/")
def display_index():
    return "Hello World!"