# Hands On Keycloak

Picture this: you’ve built the Mona Lisa of web apps. It’s sleek, responsive, and your mom already told all her friends about it. 
But there’s a problem—who’s sneaking in? The neighbor’s cat? Your ex? The bots plotting to sell your user data?

Enter Keycloak, the bouncer your web app deserves. 
Keycloak doesn’t just stand at the door checking IDs—it’s the ultimate gatekeeper, ready to keep out the riffraff while handing VIP badges to your legitimate users. 
With just a few configurations, it turns your app into a fortress, complete with identity management, single sign-on (SSO), and all the cool acronyms you can dream of.

In this guide, we’ll show you how to integrate Keycloak into your app, step by step, without needing a master’s degree in security wizardry. 
Think of it as the IKEA of authentication setups—minimal tools, clear-ish instructions, and the occasional head-scratch. 
By the end, your app will have more swagger than a nightclub with a velvet rope. Let’s dive in!

## Step 1: Setup Simple Web App
Alright, it’s time to roll up our sleeves and get down to business. Before Keycloak can work its magic, we need a web app that’s ready to welcome it with open arms (and a solid codebase). Think of this as setting up the stage for Keycloak to come in and steal the show.  

### Gather Your Ingredients  

We’re keeping it simple here—a lightweight Flask app with just enough sauce to showcase Keycloak’s power. First, let’s get those dependencies in line:  

`requirements.txt`:  
```text
Flask==3.1.0
Jinja2==3.1.4
Authlib==1.3.2
python-keycloak==5.1.1
```
Why these? Flask is our go-to for quick and clean web apps, Jinja2 handles the templating, and Authlib plus python-keycloak will help us tango with Keycloak like pros.
### Hello, Flask!

Next, whip up a simple `app.py` to get the app running:
```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def display_index():
    return "Hello World!"
```
This is your web app equivalent of “Hello, it’s me.” Nothing fancy, but hey, every masterpiece starts with a blank canvas.

### Fire It Up
Now it’s time to see our baby take its first steps. Follow these commands:
```shell
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask run
```
If everything goes smoothly, you’ll see your app live at http://127.0.0.1:5000. 
Open it up in your browser, and there it is: a humble “Hello World!” waiting to grow into something much cooler.

## Step 2: Dockerize your app

So, your app is running locally, and you’re feeling like a coding wizard. 
But let’s be honest—what’s the point if it can’t break free from your laptop and live its best life in the cloud (or at least on a server)? 
It’s time to put that app into a Docker container and make it portable, scalable, and just downright cool.

### Write a Dockerfile  

A `Dockerfile` is like a recipe for building a gourmet app container. Here’s what it looks like for our Flask app:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
```

Let’s break it down:
 - **Base Image**: We’re using python:3.13-slim—lightweight, fast, and all the Python goodness.
 - **Working Directory**: /app is where all the magic will happen inside the container.
 - **Dependencies**: We copy requirements.txt and install everything with pip.
 - **Code**: The app.py gets dropped into the container like a star actor onto a stage.
 - **Expose the Port**: Flask defaults to port 5000, so we make it visible to the outside world.
 - **Run the App**: The final CMD starts the show.

### Add Docker Compose

Why stop at a container when you can orchestrate it like a symphony? 
Docker Compose is here to make life easier, especially if you add a database or other services down the line. 
Here’s a simple docker-compose.yml:

docker-compose.yml:
```yaml
version: '3.9'

services:
  app:
    build:
      context: ./
    ports:
      - "80:5000"
```

This does two key things:
 - **Builds the Image**: It points to your Dockerfile and takes care of building the app.
 - **Maps Ports**: It maps port 5000 inside the container to port 80 on your machine, so your app is accessible at http://localhost.

### Fire Up Your App in Docker

Once your Dockerfile and docker-compose.yml are in place, you’re just one command away from greatness:

```shell
docker compose up -d
```

This command builds your image, starts the container, and detaches it (hence the -d). 
To check that it's running, navigate to http://localhost in your browser, and voila! 
Your app is now running inside a Docker container. 
The “Hello World!” is still humble, but now it’s got a passport to travel anywhere Docker is allowed.

## Step 3: Secure your useless app with Keycloak

Congrats, you’ve built the perfect playground for Keycloak to show off its skills. 
In this section, we’ll bring in the bouncer, set up the ID checks, and make sure no shady characters sneak past the door. 
Buckle up—it’s about to get fun!






## TODO:
- confirm that this should be focused on some random minimal example app not reddyt
- confirm that this should be reproducible but not a step by step tutorial
