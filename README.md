# Reddyt

Reddit in bad and ugly

## Run

### Only flask app

> #### Prerequisites
> - Phyton 3.13

*Setup:*
```shell
cd reddyt-app
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

*Start flask:*
```shell
python3 -m flask run
```

### Docker
```shell
docker compose up
```


## Possible additional technologies

 - keycloak
 - helm
 - Prometheus (+ Grafana)
 - Fluentd (logs)
 - Chaos Mesh (idk)