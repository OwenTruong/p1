import logging
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

ROUTERS_DIR = Path(__file__).resolve().parent
SRC_DIR = ROUTERS_DIR.parent
TEMPLATES_DIR = SRC_DIR / 'templates'

router = APIRouter(
)

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
  return templates.TemplateResponse(
    name="login.html",
    context={
      "request": request
    }
  )

@router.get("/register", status_code=200, response_class=HTMLResponse)
async def serve_register(request: Request):
  return templates.TemplateResponse(
    name="register.html",
    context={
      "request": request
    }
  )

@router.get("/protected", status_code=200, response_class=HTMLResponse)
async def serve_protected(request: Request):
  logging.info("Now serving protected page")
  return templates.TemplateResponse(
    name="protected.html",
    context={
      "request": request,
      "user": {
        "username": "John Doe"
      }
    }
  )

@router.get("/error", status_code=200, response_class=HTMLResponse)
async def serve_error(request: Request):
  return templates.TemplateResponse(
    name="error.html",
    context={
      "request": request
    }
  )