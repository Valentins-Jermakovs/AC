# =========================
# User modification service
# =========================

# Imports
# Libraries
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import re
# Models
from ...models import UserModel
# Utils
from ...utils.get_user_with_role import get_user_with_role



# =========================
# Change user email (ASYNC SAFE)
# =========================
async def change_user_email(
    user_id: int,
    new_email: str,
    db: AsyncSession
):
    """
    Changes a user's email address.
    """

    # Load user asynchronously
    user = await db.get(UserModel, user_id)

    # Normalize
    new_email = new_email.strip().lower()

    # Validate email format
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(regex, new_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    # Validation: user exists
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Validation: user active
    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )

    # Check email uniqueness (async correct way)
    result = await db.exec(
        select(UserModel).where(UserModel.email == new_email)
    )
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Update
    user.email = new_email

    # Commit async
    await db.commit()

    # Refresh async
    await db.refresh(user)

    # Return aggregated user
    return await get_user_with_role(user_id, db)