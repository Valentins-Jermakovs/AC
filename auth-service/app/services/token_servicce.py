# ===== Importi =====
import jwt
import secrets
import os
from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from dotenv import load_dotenv

from ..models.models import Token

from .password_service import *


# ===== dotenv faila satura apstrāde =====
load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# ===== Tokena ģenerācija =====
def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# ===== Refresh tokena ģenerācija =====
def create_refresh_token(): return secrets.token_urlsafe(32)


# ===== Refresh tokena saglabāšana DB =====
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