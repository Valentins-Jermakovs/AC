# === Šis serviss atbild par tokenu ģenerāciju ===
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from .password_service import *
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import secrets
from sqlmodel import Session
from ..models.models import Token

# === dotenv faila satura apstrāde un nolasīšana  ===
import os
from dotenv import load_dotenv

load_dotenv() # nolasa .env faila saturu

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# === === === === === === === === === === === === === ===

# === Tokena ģenerācija ===
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# === === === === === ===

# === Refreš tokena ģenerācija ===
def create_refresh_token():
    return secrets.token_urlsafe(32)
# === === === === ===


# === Refreš tokena saglabāšana DB ===
def save_refresh_token(refresh_token: str, user_id: int, db: Session, expires_days: int = 7):
    token = Token(
        user_id=user_id,
        refresh_token=refresh_token,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=expires_days)
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token
# === === === === === === === === === === === === === === === === === === === === === === === === ===