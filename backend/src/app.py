# System & Third Party
from pathlib import Path
import logging

from fastapi import FastAPI, Request, HTTPException, status, Response
from starlette.middleware.base import BaseHTTPMiddleware

# First Party
from src.auth import create_access_token, AuthPayload, Token, decode_and_verify_token
from src.dao import UserDAO
from src.exceptions import UserRegistrationError, InvalidCredentialsError
from src.utils.config import get_config
from src.middleware.logging import logging_middleware
from src.routers import metrics


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

config = get_config()

logging.basicConfig(level=logging.INFO if config.mode == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

user_dao = UserDAO()

app = FastAPI(title="JWT Authenticator")

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.include_router(metrics.router)

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

@app.post("/api/auth/token")
async def verify_cookie_token(request: Request):
    """
    Validates the active session token passed automatically via the 
    browser's HttpOnly Cookie storage mechanisms.
    """
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Cookie"}
        )

    try:
        token_string = access_token.replace("Bearer ", "")
        token_payload = decode_and_verify_token(token_string)
        return {
            "status": "success",
            "username": token_payload.get("sub")
        }
    
    except HTTPException as exc:
        raise exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed or invalid authorization token signature",
            headers={"WWW-Authenticate": "Cookie"}
        )