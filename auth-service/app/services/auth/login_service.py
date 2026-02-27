# =========================
# Authentication service (ASYNC)
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
# Models
from ...models import UserModel, TokenModel
# Password utility
from ..passwords.passwords_service import verify_password
# Token management
from ..tokens_management.create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)
# Schemas
from ...schemas.auth.login_schema import LoginSchema
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema


# =========================
# User login
# =========================
async def login_user(
    db: AsyncSession,
    data: LoginSchema
) -> TokenRefreshSchema:

    # Normalize username
    data.username = data.username.lower()

    # =========================
    # Find user
    # =========================
    result = await db.exec(
        select(UserModel).where(UserModel.username == data.username)
    )
    user = result.first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid data")

    user = user

    # =========================
    # Verify password
    # =========================
    if not await verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid data")

    # =========================
    # Check active
    # =========================
    if not user.active:
        raise HTTPException(status_code=401, detail="Invalid data")

    # =========================
    # Delete old refresh tokens
    # =========================
    result = await db.exec(
        select(TokenModel).where(TokenModel.user_id == user.id)
    )
    old_tokens = result.all()

    for t in old_tokens:
        await db.delete(t)

    await db.commit()

    # =========================
    # Generate new tokens
    # =========================
    refresh_token_value = await create_refresh_token()

    await save_refresh_token(refresh_token_value, user.id, db)

    access_token = await create_access_token({
        "sub": str(user.id)
    })

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )