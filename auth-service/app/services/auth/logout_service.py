# =========================
# Logout service (ASYNC)
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
# Models
from ...models import TokenModel


async def logout(
    db: AsyncSession,
    refresh_token: str
) -> dict:
    """
    Invalidates refresh token by deleting it from database.
    """

    # Find token
    result = await db.exec(
        select(TokenModel).where(TokenModel.refresh_token == refresh_token)
    )

    token = result.first()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    await db.delete(token)

    await db.commit()

    return {"message": "Logout successful"}