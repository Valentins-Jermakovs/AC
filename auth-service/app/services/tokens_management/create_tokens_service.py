# =========================
# Token Management Service
# =========================

import jwt
import secrets
import os
from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from dotenv import load_dotenv
from ...models import Token


# =========================
# Load environment variables
# =========================
load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# =========================
# Create JWT Access Token
# =========================
def create_access_token(
    data: dict, 
    expires_delta: timedelta | None = None
) -> str:
    """
    Generates a JWT access token.

    Steps:
    1. Copy input data to avoid mutation
    2. Set expiration time
       - Use provided expires_delta if given
       - Otherwise use default ACCESS_TOKEN_EXPIRE_MINUTES from env
    3. Add "exp" claim to payload
    4. Encode JWT with SECRET_KEY and ALGORITHM
    5. Return encoded JWT string

    :param data: Payload dictionary (e.g., {"sub": user_id})
    :param expires_delta: Optional custom expiration timedelta
    :return: JWT access token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# =========================
# Create Refresh Token
# =========================
def create_refresh_token() -> str:
    """
    Generates a secure random refresh token.

    Uses Python's secrets module for cryptographic randomness.

    :return: Refresh token string
    """
    return secrets.token_urlsafe(32)


# =========================
# Save Refresh Token to DB
# =========================
def save_refresh_token(
    refresh_token: str, 
    user_id: int, 
    db: Session, 
    expires_days: int = 7
) -> Token:
    """
    Saves a refresh token for a user in the database.

    Steps:
    1. Create Token object with user_id, refresh_token, created_at, expires_at
    2. Add token to database session
    3. Commit changes
    4. Refresh object to get updated DB fields
    5. Return Token object

    :param refresh_token: The token string to save
    :param user_id: ID of the user
    :param db: Database session
    :param expires_days: Optional expiration in days (default 7)
    :return: Token object saved in DB
    """
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