FROM python:3.13-slim

# install nginx and npm
RUN apt-get update && apt-get install -y nginx

WORKDIR /app

# configure nginx
COPY nginx.conf /etc/nginx/sites-available/flask-app.conf
RUN ln -s /etc/nginx/sites-available/flask-app.conf /etc/nginx/sites-enabled
RUN rm -f /etc/nginx/sites-enabled/default

# install python app dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# configure worker scale
ARG WORKER_SCALE=4
ENV WORKER_SCALE ${WORKER_SCALE}

EXPOSE 80

CMD nginx \
    && echo 'nginx is running now on http://localhost:80' \
    && gunicorn -w ${WORKER_SCALE} -b localhost:5000 --log-level=debug 'reddyt-app.app:start(True)'

#EXPOSE 5000
#CMD ["flask", "run", "--host=0.0.0.0"]