# =========================
# Token Management Service (ASYNC)
# =========================

# Imports
# Libraries
import jwt
import secrets
import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
# Models
from ...models import TokenModel
# Utils
from ...utils.current_date import get_current_date


# =========================
# Load environment variables
# =========================
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
)


# ============================================================
# Create JWT Access Token
# ============================================================

async def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = get_current_date() + expires_delta
    else:
        expire = get_current_date() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ============================================================
# Create Refresh Token
# ============================================================

async def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)


# ============================================================
# Save Refresh Token (ASYNC)
# ============================================================

async def save_refresh_token(
    refresh_token: str,
    user_id: int,
    db: AsyncSession,
    expires_days: int = 7
) -> TokenModel:

    token = TokenModel(
        user_id=user_id,
        refresh_token=refresh_token,
        created_at=get_current_date(),
        expires_at=get_current_date() + timedelta(days=expires_days)
    )

    db.add(token)

    await db.commit()
    await db.refresh(token)

    return token


# ============================================================
# Delete Refresh Token (ASYNC)
# ============================================================

async def delete_refresh_token(
    refresh_token: str,
    db: AsyncSession
) -> None:

    result = await db.exec(
        select(TokenModel).where(
            TokenModel.refresh_token == refresh_token
        )
    )

    rows = result.all()

    for row in rows:
        token_obj = row[0]
        await db.delete(token_obj)

    await db.commit()