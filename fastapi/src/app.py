
# System & Third Party
from fastapi import FastAPI, Request, Depends, HTTPException, status
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="JWT Authenticator")
