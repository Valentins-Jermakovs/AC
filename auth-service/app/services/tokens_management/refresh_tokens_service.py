# =========================
# Refresh Service
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from ...models import Token, User
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema
from .create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


# =========================
# Load environment variables
# =========================
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# =========================
# Decode access token
# =========================
async def check_access_token(access_token: str) -> int:
    """
    Decodes a JWT access token and returns the user ID.

    Steps:
    1. Decode JWT using SECRET_KEY and ALGORITHM
    2. Extract user_id from 'sub' claim
    3. Raise HTTP 401 if token is expired or invalid

    :param access_token: JWT token string
    :return: user_id (int) from token
    :raises HTTPException: 401 if token expired or invalid
    """
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

# =========================
# Refresh access token using refresh token
# =========================
async def refresh_access_token(
    refresh_token: str,
    db: Session
) -> TokenRefreshSchema:
    """
    Validates a refresh token and returns new access and refresh tokens.

    Steps:
    1. Look up the refresh token in DB
       - Raise 401 if token does not exist
    2. Check expiration of refresh token
       - Delete token and raise 401 if expired
    3. Check if associated user exists and is active
       - Raise 401 if user inactive or missing
    4. Delete old refresh token (rotation)
    5. Create and save a new refresh token
    6. Create a new access token
    7. Return TokenRefreshSchema with new tokens

    :param refresh_token: Refresh token string
    :param db: SQLModel database session
    :return: TokenRefreshSchema containing access_token, token_type, refresh_token
    :raises HTTPException: 401 if refresh token invalid/expired or user inactive
    """
    # Fetch refresh token from DB
    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Check expiration
    expires_at = token.expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        db.delete(token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    # Check user exists and active
    user = db.exec(
        select(User).where(User.id == token.user_id)
    ).first()

    if not user or not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or does not exist"
        )

    # Token rotation: delete old refresh token
    db.delete(token)
    db.commit()

    # Generate new refresh token and save
    new_refresh_token = create_refresh_token()
    save_refresh_token(new_refresh_token, token.user_id, db)
    
    # Generate new access token
    access_token = create_access_token({"sub": str(token.user_id)})

    # Return tokens
    return TokenRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=new_refresh_token
    )