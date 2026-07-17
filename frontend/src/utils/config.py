
import os
from dotenv import load_dotenv

from src.data.config import Config

load_dotenv()

__config = Config(
  mode= "Production" if os.getenv("MODE") == "Production" else "Development",
  backend_url=os.getenv("BACKEND_URL", "10.0.1.254"),
  fastapi_port=int(os.getenv("FASTAPI_PORT", 8080))
)

def get_config():
  return __config