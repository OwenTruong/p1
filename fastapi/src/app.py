
# System & Third Party
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pathlib import Path
from dotenv import load_dotenv

from src.auth import create_access_token, decode_and_verify_token, AuthPayload, Token
from src.dao import UserDAO
from src.exceptions import UserRegistrationError, InvalidCredentialsError

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

user_dao = UserDAO()
security = HTTPBearer()

app = FastAPI(title="JWT Authenticator")

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
async def register_account(payload: AuthPayload):
    try:
        user_dao.create_user(username=payload.username, password=payload.password)
        return {"status": "success", "detail": f"Account for user `{payload.username}` has been provisioned"}
    except UserRegistrationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/api/auth/login", response_model=Token)
async def login_and_issue_token(payload: AuthPayload):
    """Verifies profile match over database and issue JWT"""
    try:
        user_dao.authenticate_user(username=payload.username, password=payload.password)

        secure_token = create_access_token(username=payload.username)
        return {"access_token": secure_token, "token_type": "bearer"}
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail=str(exc))