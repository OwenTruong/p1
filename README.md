# P0 Project for Revature

See [guidelines](./docs/Guidelines.md) for more detail.


## How to run for local development

For our project, there are three different services that need to be started
* Database (PostgreSQL)
* Backend (Uvicorn FastAPI)
* Frontend (Uvicorn FastAPI)

Run the following for local development:
```bash
# Create the env file for docker
cp database/.env.example database/.env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

docker compose -f database/dev.compose.yml up -d
docker compose -f backend/dev.compose.yml up --build -d
docker compose -f frontend/compose.yml up --build -d
```

To check the logs in each service, run `compose logs` like the example below:
```bash
docker compose -f database/dev.compose.yml logs -f
```

## How to run for production

### For Azure VM Database

Clone the project.
```bash
git clone <project>
```

Install all of the docker dependencies.
```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER && newgrp docker
```

Fetch the .env file from Azure Key Vault.
```bash
cd p1/database
python3 ./getkeyvault.py
```

Run the database.
```bash
docker compose up -d
```

### For Azure VM Backend

Clone the project.
```bash
git clone <project>
```

Install all of the docker dependencies.
```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER && newgrp docker
```

Fetch the .env file from Azure Key Vault.
```bash
cd p1/backend
python3 ./getkeyvault.py
```

Build and run the backend.
```bash
docker compose up --build -d
```

### For Azure VM Frontend

Clone the project.
```bash
git clone <project>
```

Install all of the docker dependencies.
```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER && newgrp docker
```

Fetch the .env file from Azure Key Vault.
```bash
cd p1/frontend
python3 ./getkeyvault.py
```

Build and run the frontend.
```bash
docker compose up --build -d
```