import logging
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

ROUTERS_DIR = Path(__file__).resolve().parent
SRC_DIR = ROUTERS_DIR.parent
TEMPLATES_DIR = SRC_DIR / 'templates'

router = APIRouter()

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/", status_code=200, response_class=HTMLResponse)
async def serve_home(request: Request):
  return templates.TemplateResponse(
    name="index.html",
    context={
      "request": request
    }
  )

@router.get("/login", status_code=200, response_class=HTMLResponse)
async def serve_login(request: Request):
  if request.state.authorization.is_authenticated:
    return RedirectResponse('/protected')
  return templates.TemplateResponse(
    name="login.html",
    context={
      "request": request
    }
  )

@router.get("/register", status_code=200, response_class=HTMLResponse)
async def serve_register(request: Request):
  if request.state.authorization.is_authenticated:
    return RedirectResponse('/protected')
  return templates.TemplateResponse(
    name="register.html",
    context={
      "request": request
    }
  )

@router.get("/protected", status_code=200, response_class=HTMLResponse)
async def serve_protected(request: Request):
  if not request.state.authorization.is_authenticated:
    query = {
      "error_name": "Status 403",
      "error_message": request.state.authorization.error_message or ''
    }
    return RedirectResponse(url=f"/error?{urlencode(query)}")
  logging.info("Now serving protected page")
  return templates.TemplateResponse(
    name="protected.html",
    context={
      "request": request,
      "user": {
        "username": request.state.authorization.username
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