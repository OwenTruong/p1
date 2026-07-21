# System & Third Party
import time
from pathlib import Path
import logging
import traceback
import os

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from requests import request


# First Party
from src.routers import web
from src.utils.config import get_config
from src.middlewares.check_auth_state import check_auth_status
from src.middlewares.logging_middleware import logging_middleware

config = get_config()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

logging.basicConfig(level=logging.INFO if config.mode == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="JWT Authenticator")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=check_auth_status)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

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

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_account(payload: dict):
    url=f"http://{config.backend_url}/api/auth/register"
    logging.info(f"Forwarding user registration to {url} with username {payload.get('username', None)}")
    resp = request('POST', url, json=payload)
    
    if resp.status_code >= 400:
        logging.warning(f"Backend ({url}) returned with status code ({resp.status_code}) with message ({resp.text})")
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return resp.json()

@app.post("/api/auth/login", status_code=status.HTTP_200_OK)
def login_and_issue_token(payload: dict, response: Response):
    url=f"http://{config.backend_url}/api/auth/login"
    logging.info(f"Forwarding user login to {url} with username {payload.get('username', None)}")

    resp = request('POST', url, json=payload)

    if resp.status_code >= 400:
        logging.warning(f"Backend ({url}) returned with status code ({resp.status_code}) with message ({resp.text})")
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    
    for set_cookie in resp.raw.headers.get_all("Set-Cookie") or []:
        response.headers.append("set-cookie", set_cookie)
    
    return resp.json()
    
@app.post("/api/auth/logout", status_code=status.HTTP_200_OK)
def logout(req: Request, response: Response):
    url=f"http://{config.backend_url}/api/auth/logout"
    logging.info(f"Forwarding user logout to {url}")

    resp = request('POST', url, cookies={
        "access_token": req.cookies.get('access_token', '')
    })

    if resp.status_code >= 400:
        logging.warning(f"Backend ({url}) returned with status code ({resp.status_code}) with message ({resp.text})")
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    for set_cookie in resp.raw.headers.get_all("Set-Cookie") or []:
        response.headers.append("set-cookie", set_cookie)


    return resp.json()
