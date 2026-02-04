from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session
from dotenv import load_dotenv

import os

from ..services.google_service import google_auth_callback, get_google_auth

from ..dependencies.data_base_connection import get_db

load_dotenv()
# http://localhost:8000/auth/google/login
router = APIRouter(prefix="/auth/google", tags=["Google"])

# === OAuth ===
oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile",
    },
)

@router.get("/login")
async def login(request: Request):
    return await get_google_auth(oauth, request)

@router.get("/callback")
async def auth_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    return await google_auth_callback(oauth, db, request)
