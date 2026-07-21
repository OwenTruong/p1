import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOG_DIR / "middleware.json"


azure_logger = logging.getLogger("middleware_json_logger")
azure_logger.setLevel(logging.INFO)
azure_logger.propagate = False

json_file_handler = RotatingFileHandler(
    filename=str(LOG_FILE_PATH),
    maxBytes=10 * 1024 * 1024,  # 10 MB per log file
    backupCount=3
)

json_file_handler.setFormatter(logging.Formatter('%(message)s'))
azure_logger.addHandler(json_file_handler)