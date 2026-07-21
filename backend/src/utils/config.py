import os
from dotenv import load_dotenv

from src.data.config import Config

load_dotenv()

# intentionally using invalid defaults to find error in config if any
__config = Config(
  db_host = os.getenv("DB_HOST", "10.0.3.254"),
  db_name = os.getenv("DB_NAME", "my_db"),
  db_user = os.getenv("DB_USER", "my_db_user"),
  db_password = os.getenv("DB_PASSWORD", "MyPassword1234"),

  mode = "Production" if os.getenv("MODE") == "Production" else "Development",
  jwt_secret_key = os.getenv("JWT_SECRET_KEY", "MySecret1234"),
  jwt_algorithm = os.getenv("JWT_ALGORITHM", "N/A"),
  backend_port = int(os.getenv("FRONTEND_PORT", 8080))
)

def get_config():
  return __config