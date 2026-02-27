# =========================
# User retrieval service
# =========================

# Imports
# Libraries
from sqlmodel import select
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
# Models
from ...models import UserModel
# Schemas
from ...schemas.users.user_schema import UserSchema
# Utils
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get user by ID
# =========================
async def get_user_by_id(
    user_id: int,
    db: AsyncSession
) -> UserSchema:

    # Proper async query
    result = await db.exec(
        select(UserModel).where(UserModel.id == user_id)
    )

    # In async SQLModel this returns User object (not tuple)
    user = result.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Roles (async)
    roles_map = await get_users_roles_map(user_id, db)
    user_roles = roles_map.get(user.id, [])

    # NEVER modify ORM object
    created_at_str = (
        user.created_at.strftime("%Y-%m-%d")
        if user.created_at
        else None
    )

    return UserSchema(
        id=user.id,
        username=user.username or "",
        email=user.email,
        active=user.active,
        roles=user_roles,
        created_at=created_at_str
    )