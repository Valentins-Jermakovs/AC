# =========================
# Authentication service
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException
# Database models
from ...models import User, Token
# Password utility
from ..passwords.passwords_service import verify_password
# Token management utilities
from ..tokens_management.create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)
# Request and response schemas
from ...schemas.auth.login_schema import LoginSchema
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema


# =========================
# User login
# =========================
async def login_user(db: Session, data: LoginSchema) -> TokenRefreshSchema:
    """
    Authenticates a user by username and password, and generates new tokens.

    Steps:
    1. Normalize username to lowercase
    2. Find user in database
       - Raises 401 if user not found
    3. Verify password
       - Raises 401 if password invalid
    4. Check if user is active
       - Raises 401 if inactive
    5. Delete old refresh tokens (token rotation)
    6. Generate new refresh and access tokens
    7. Return tokens in TokenRefreshSchema

    :param db: SQLModel database session
    :param data: LoginSchema containing username and password
    :return: TokenRefreshSchema containing access_token, token_type, refresh_token
    :raises HTTPException: 401 if authentication fails
    """

    # Convert username to lowercase for consistent lookup
    data.username = data.username.lower()

    # Find user in database
    user = db.exec(
        select(User).where(User.username == data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Verify password hash
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Check if user is active
    if not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")


    # Delete old refresh tokens for this user
    old_tokens = db.exec(select(Token).where(Token.user_id == user.id)).all()
    for t in old_tokens:
        db.delete(t)
    db.commit()


    # Generate new refresh token and save to DB
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)

    # Generate new access token
    access_token = create_access_token({
        "sub": str(user.id)
    })

    # Return token response
    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )