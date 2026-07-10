
# System & Third Party
import time
from pathlib import Path
from dotenv import load_dotenv
import logging
import os

from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles

# First Party
from .routers import web

from src.auth import create_access_token, AuthPayload, Token
from src.dao import UserDAO
from src.exceptions import UserRegistrationError, InvalidCredentialsError

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'
MODE = os.getenv("MODE", "production")

logging.basicConfig(level=logging.INFO if MODE == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

user_dao = UserDAO()

app = FastAPI(title="JWT Authenticator")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.middleware("http")
async def log_request_execution_latency(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    logging.info(f"HTTP {request.method} {request.url.path} processed in {time.time() - start_time:.4f}s")
    return response

@app.middleware("http")
async def check_auth_status(request: Request, call_next):
   response = await call_next(request)
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

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
async def register_account(payload: AuthPayload):
    try:
        user_dao.create_user(username=payload.username, password=payload.password)
        return {"status": "success", "detail": f"Account for user `{payload.username}` has been provisioned"}
    except UserRegistrationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/api/auth/login", response_model=Token)
async def login_and_issue_token(payload: AuthPayload, response: Response):
    """Verifies profile match over database and issue JWT"""
    try:
        user_dao.authenticate_user(username=payload.username, password=payload.password)
        secure_token = create_access_token(username=payload.username)
        
        response.set_cookie(
            key="access_token",
            value=f"Bearer {secure_token}",
            httponly=True,        # Prevents JavaScript access (XSS defense)
            max_age=900,         # Cookie life in seconds (15 mins)
            expires=900,
            samesite="lax",       # Protects against CSRF in common scenarios
            secure=False,         # Set to True in production (requires HTTPS)
        ) 
        
        return {"status": "success", "detail": "Successfully authenticated session"}
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    
@app.post("/api/auth/logout", status_code=200)
async def logout(response: Response):
    """Instructs client browser to purge the active HttpOnly session token"""
    response.delete_cookie(key="access_token", httponly=True, samesite="lax", secure=False,)
    return {"status": "success", "detail": "Session cookie cleared"}
