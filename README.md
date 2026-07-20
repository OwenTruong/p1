# P0 Project for Revature

See [guidelines](./docs/Guidelines.md) for more detail.


## How to run for local development

We have separated docker files into two types to prevent rebuilding images over and over again for local development:
* Local
  * `dev.compose.yml`
  * `Dockerfile.dev`
* Production
  * `prod.compose.yml`
  * `Dockerfile.prod`

Run the following to setup fastapi docker for local development:
```bash
cd fastapi
docker compose -f dev.compose.yml build
docker compose -f dev.compose.yml up -d
```

Run the following afterwards to restart container when there are new changes in `/fastapi/`
```bash
docker compose -f dev.compose.yml restart
```

The backend relies on a working database, therefore run the following to setup database docker for local development:
```bash
docker network create app_network
cd database
docker compose -f dev.compose.yml up --build
```
then in a new terminal run following command to setup backend docker:
```bash
cd backend
docker compose -f dev.compose.yml up --build
```

## How to run for production

Run the following to setup for Azure VM:
```bash
git clone <project>
```
```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER && newgrp docker

cd p1/fastapi
python3 ./getkeyvault.py
docker compose -f prod.compose.yml build
docker compose -f prod.compose.yml up -d
```
