# ===========================
# User search service (ASYNC)
# ===========================

# Imports
# Libraries
from sqlmodel import select
from sqlalchemy import or_
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
import re
# Models
from ...models import UserModel
# Schemas
from app.schemas.users.user_by_email_schema import UserByEmailSchema

# =========================
# Search users by email
# =========================
async def get_by_email(
    email: str,
    db: AsyncSession
):
    # Validate email
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(regex, email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    # Normalize
    email = email.strip().lower()

    # Proper async query
    result = await db.exec(
        select(UserModel).where(UserModel.email == email)
    )

    # In async SQLModel this returns User object (not tuple)
    user = result.one_or_none()

    # Validation
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return data
    return UserByEmailSchema(
        id=user.id,
        email=user.email
    )