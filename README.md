# Reddyt

Reddit in bad and ugly

## Run

### Only flask app

> #### Prerequisites
> - Phyton 3.13

```shell
cd reddyt-app
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
env FLASK_APP=reddyt-app.app:start
python3 -m flask run
```

### Docker
```shell
docker compose up
```