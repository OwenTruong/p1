import logging
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.auth import decode_and_verify_token

ROUTERS_DIR = Path(__file__).resolve().parent
SRC_DIR = ROUTERS_DIR.parent
TEMPLATES_DIR = SRC_DIR / 'templates'

router = APIRouter()

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

class Authorization(BaseModel):
  is_authenticated: bool = Field(default=False, examples=[True, False])
  username: str | None = Field(default=None, examples=[None, "test_dev"])
  error_message: str | None = Field(default=None, examples=[None, 'Session has expired. Please re-authenticate'])

def get_auth_status(request: Request) -> Authorization:
  access_token = request.cookies.get("access_token", None)
  if not access_token:
    return Authorization(is_authenticated=False, username=None, error_message="No access token provided.")

  try:
    token_string = access_token.replace("Bearer ", "")
    token_payload = decode_and_verify_token(token_string)
    return Authorization(is_authenticated=True, username=token_payload.get("sub"), error_message=None)
  except HTTPException as exc:
    return Authorization(is_authenticated=False, username=None, error_message=exc.detail)
  except Exception:
    return Authorization(is_authenticated=False, username=None, error_message="Internal Server Error")


@router.get("/", status_code=200, response_class=HTMLResponse)
async def serve_home(request: Request):
  return templates.TemplateResponse(
    name="index.html",
    context={"request": request}
  )

@router.get("/login", status_code=200, response_class=HTMLResponse)
async def serve_login(request: Request, authorization: Authorization = Depends(get_auth_status)):
  if authorization.is_authenticated:
    return RedirectResponse('/protected')
  return templates.TemplateResponse(
    name="login.html",
    context={"request": request}
  )

@router.get("/register", status_code=200, response_class=HTMLResponse)
async def serve_register(request: Request, authorization: Authorization = Depends(get_auth_status)):
  if authorization.is_authenticated:
    return RedirectResponse('/protected')
  return templates.TemplateResponse(
    name="register.html",
    context={"request": request}
  )

@router.get("/protected", status_code=200, response_class=HTMLResponse)
async def serve_protected(request: Request, authorization: Authorization = Depends(get_auth_status)):
  if not authorization.is_authenticated:
    query = {
      "error_name": "Status 403",
      "error_message": authorization.error_message or ''
    }
    return RedirectResponse(url=f"/error?{urlencode(query)}")
  logging.info("Now serving protected page")
  return templates.TemplateResponse(
    name="protected.html",
    context={
      "request": request,
      "user": {
        "username": authorization.username
      }
    }
  )

@router.get("/error", status_code=200, response_class=HTMLResponse)
async def serve_error(request: Request, error_name: str = 'Status 500', error_message: str = ''):
  return templates.TemplateResponse(
    name="error.html",
    context={
      "request": request,
      "error": {
        "name": error_name,
        "message": error_message
      }
    }
  )