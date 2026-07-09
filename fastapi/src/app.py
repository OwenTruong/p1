
# System & Third Party
import time
from pathlib import Path
from dotenv import load_dotenv
import logging
import os

from fastapi import FastAPI, HTTPException, Request

# First Party
from .routers import web

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'
MODE = os.getenv("MODE", "production")

logging.basicConfig(level=logging.INFO if MODE == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="JWT Authenticator")

@app.middleware("http")
async def log_request_execution_latency(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  logging.info(f"HTTP {request.method} {request.url.path} processed in {time.time() - start_time:.4f}s")
  return response


app.include_router(web.router)

@app.get("/health", status_code=200)
async def get_health():
  """Used to check if API is running"""
  try:
    return {
      "status": "healthy",
    }
  except Exception as exc:
    raise HTTPException(status_code=500, detail=str(exc))
  