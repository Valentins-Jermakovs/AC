# Imports
import jwt
import secrets
import os
from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from dotenv import load_dotenv
from ...models import Token

"""
Token Service

This module provides functionality for generating, saving, and managing authentication tokens.

Functions:

1. create_access_token(data: dict, expires_delta: timedelta | None = None) -> str
   - Purpose: Generates a JWT access token for a user.
   - Input: 
       - data: Dictionary containing payload data (e.g., user ID).
       - expires_delta: Optional custom expiration time; defaults to ACCESS_TOKEN_EXPIRE_MINUTES from env.
   - Output: Encoded JWT access token as a string.
   - Notes: Adds "exp" claim for expiration.

2. create_refresh_token() -> str
   - Purpose: Generates a secure random refresh token.
   - Output: Refresh token string.
   - Notes: Uses Python's secrets module to ensure cryptographic randomness.

3. save_refresh_token(refresh_token: str, user_id: int, db: Session, expires_days: int = 7) -> Token
   - Purpose: Saves a refresh token in the database for a specific user.
   - Input: 
       - refresh_token: The token string to save.
       - user_id: ID of the user owning the token.
       - db: SQLModel Session for database operations.
       - expires_days: Optional expiration period for the refresh token (default 7 days).
   - Output: Token object representing the saved token.
   - Notes: Sets creation and expiration timestamps and commits the token to the database.

Environment:
- SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES are loaded from a .env file.
"""


# dotenv file contents read
load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Access token generator
def create_access_token(data: dict, expires_delta: timedelta | None = None):

    # set and user id
    to_encode = data.copy()

    # check if expires_delta is set
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # set and expire time
    to_encode.update({"exp": expire})
    # encode
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Refresh token generator
def create_refresh_token(): return secrets.token_urlsafe(32)


# Refresh token saver
def save_refresh_token(refresh_token: str, user_id: int, db: Session, expires_days: int = 7):

    # Create token
    token = Token(
        user_id=user_id,
        refresh_token=refresh_token,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=expires_days)
    )

    # Save token to database
    db.add(token)
    db.commit()
    db.refresh(token)

    return token