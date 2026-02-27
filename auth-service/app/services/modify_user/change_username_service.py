# =========================
# User modification service
# =========================

# Imports
# Libraries
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
# Models
from ...models import UserModel
# Utils
from ...utils.get_user_with_role import get_user_with_role

# =========================
# Change user username
# =========================
async def change_user_username(
    user_id: int,
    new_username: str,
    db: AsyncSession
):
    """
    Changes a user's username.

    Validation and behavior:
    1. Load user by ID
       - Raises 404 if user not found
       - Raises 403 if user is inactive
    2. Normalize new username (strip & lowercase)
    3. Check if username already exists
       - Raises 400 if duplicate
    4. Update username in database
    5. Commit changes and refresh user object
    6. Return user data with roles

    :param user_id: ID of the user to update
    :param new_username: New username string
    :param db: Database session
    :return: UserSchema with updated username and roles
    :raises HTTPException: 404 if user not found, 403 if inactive, 400 if username exists
    """

    user = await db.get(UserModel, user_id)

    new_username = new_username.strip().lower()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    result = await db.exec(
        select(UserModel).where(UserModel.username == new_username)
    )
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user.username = new_username

    await db.commit()
    await db.refresh(user)

    return await get_user_with_role(user_id, db)