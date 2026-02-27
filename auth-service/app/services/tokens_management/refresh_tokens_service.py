# =========================
# Refresh Service
# =========================

# Imports
# Libraries
from sqlmodel import select
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from sqlmodel.ext.asyncio.session import AsyncSession
# Models
from ...models import TokenModel, UserModel
# Schemas
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema
# Services
from .create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


# =========================
# Load env
# =========================
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# =====================================================
# Decode access token
# =====================================================
async def check_access_token(access_token: str) -> int:
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # Get user ID from token payload ("sub" = subject)
        user_id = payload.get("sub")

        return int(user_id)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# =====================================================
# Refresh tokens
# =====================================================
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession
) -> TokenRefreshSchema:

    result = await db.exec(
        select(TokenModel).where(
            TokenModel.refresh_token == refresh_token
        )
    )

    token = result.first()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    # expiration check
    expires_at = token.expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        await db.delete(token)
        await db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    # check user
    user_result = await db.exec(
        select(UserModel).where(UserModel.id == token.user_id)
    )

    user = user_result.first()

    if not user or not user.active:
        raise HTTPException(
            status_code=401,
            detail="User inactive"
        )

    # token rotation
    await db.delete(token)
    await db.commit()

    new_refresh_token = await create_refresh_token()
    await save_refresh_token(new_refresh_token, token.user_id, db)

    access_token = await create_access_token(
        {"sub": str(token.user_id)}
    )

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=new_refresh_token
    )