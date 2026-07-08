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