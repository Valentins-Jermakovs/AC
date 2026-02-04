# Imports
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


"""
Refresh Service

This module provides functionality for validating access tokens and refreshing them using refresh tokens.

Functions:

1. get_user_id_from_access_token(token: str) -> int
   - Purpose: Decodes a JWT access token to extract the user ID.
   - Input: JWT access token as a string.
   - Output: User ID (int) from the token payload.
   - Raises:
       - HTTP 401 if the token has expired or is invalid.

2. refresh_access_token(refresh_token: str, db: Session = Depends(get_db)) -> TokenWithRefreshSchema
   - Purpose: Rotates a refresh token and generates a new access token.
   - Input:
       - refresh_token: Refresh token string provided by the client.
       - db: SQLModel Session injected via dependency injection.
   - Output: TokenWithRefreshSchema containing new access_token, token_type, and refresh_token.
   - Process:
       1. Validates the refresh token exists and is not expired.
       2. Checks the associated user exists and is active.
       3. Deletes the old refresh token (rotation).
       4. Generates a new refresh token and saves it.
       5. Generates a new access token.
   - Raises:
       - HTTP 401 if the refresh token is invalid, expired, or the user is inactive/nonexistent.

Environment:
- SECRET_KEY and ALGORITHM are loaded from a .env file for JWT operations.
"""

# dotenv file contents read
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Access token check
async def check_access_token(access_token: str) -> int:

    # Token decode
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        

    # Error handling
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    # Error handling
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

# Access token refresh
async def refresh_access_token(
    refresh_token: str,
    db: Session
) -> TokenRefreshSchema:

    # Refresh token check
    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    # Error handling
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    expires_at = token.expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        db.delete(token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    user = db.exec(
        select(User).where(User.id == token.user_id)
    ).first()

    if not user or not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or does not exist"
        )

    # ROTATION
    db.delete(token)
    db.commit()

    # New refresh token
    new_refresh_token = create_refresh_token()
    save_refresh_token(new_refresh_token, token.user_id, db)
    # New access token
    access_token = create_access_token({
        "sub": str(token.user_id)
    })

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=new_refresh_token
    )