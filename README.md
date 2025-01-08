# Reddyt

Reddit in bad and uglY

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
docker compose up -d
```

During development the image can be re-build and -deployed with
```shell
docker compose up -d --build reddyt-app
```

To execute psql queries during development, execute
```shell
docker exec -it postgres-db /bin/psql -d blogs -U admin
```
## Possible additional technologies

 - keycloak
 - helm
 - Prometheus (+ Grafana)
 - Fluentd (logs)
 - Chaos Mesh (idk)
