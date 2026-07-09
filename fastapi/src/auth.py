import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = os.getenv("JWT_ALGORITHM", "")
TOKEN_EXPIRATION_MINUTES = 15

class AuthPayload(BaseModel):
    username: str = Field(..., examples=["test_dev"])
    password: str = Field(..., min_length=6, examples=["supersecret123"])

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str) -> str:
    """Envodes user identiy details into a cryptographically signed JWT string."""
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    # payload claims structure
    payload = {
        "sub": username, # Subject (the user identity)
        "iat": issued_at.timestamp(), # issued at timestamp
        "exp": expires_at.timestamp(), # expiration timestamp
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_and_verify_token(token: str) -> dict:
    """Decodes token payload and validates signatures and time claims"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired. Please re-authenticate",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed or invalid authorization token signature",
            headers={"WWW-Authenticate": "Bearer"}
        )