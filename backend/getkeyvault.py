import os
import json
import subprocess
from pathlib import Path

IMDS_URL="http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net"

VAULT_NAME = "kv-p1-backend-prod"
VAULT_URL = f"https://{VAULT_NAME}.vault.azure.net"

DIR_PATH = Path(__file__).resolve().parent

env_vars_li = [
  "DB_HOST",
  "DB_NAME",
  "DB_USER",
  "DB_PASSWORD",
  "MODE",
  "JWT_SECRET_KEY",
  "JWT_ALGORITHM",
  "BACKEND_PORT"
]

output = subprocess.run(["curl", "-s", "-H", "Metadata: true", IMDS_URL], capture_output=True, check=True, text=True)

key_vault_token = json.loads(output.stdout)["access_token"]
tuple_li = []

for env_var_name in env_vars_li:
  translated_env_var_name = env_var_name.replace('_', '-')
  try:
    response = subprocess.run(["curl", "-s", "-H", f"Authorization: Bearer {key_vault_token}", f"{VAULT_URL}/secrets/{translated_env_var_name}?api-version=7.4"], capture_output=True, check=True, text=True)
    value = json.loads(response.stdout)["value"]

    tuple_li.append((env_var_name, value))
  except Exception as exc:
    print(f"Failed to get env name for env var {env_var_name} and translated env var {translated_env_var_name}")
    print(str(exc.with_traceback))
    exit(1)

with open(DIR_PATH / '.env', 'w') as f:
  lines = [ f"{k}={v}\n" for k, v in tuple_li]
  f.writelines(lines)