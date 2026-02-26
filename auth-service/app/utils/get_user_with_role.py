# =========================
# User data aggregation
# =========================

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

# Database model
from ..models import User

# Response schema
from ..schemas.users.user_schema import UserSchema

# Utility that maps users to their roles
from .get_users_roles_map import get_users_roles_map


# =========================
# Get user with roles (ASYNC SAFE)
# =========================
async def get_user_with_role(
    user_id: int,
    db: AsyncSession
) -> UserSchema:
    """
    Returns user data together with assigned roles.

    Steps:
    1. Load user from database
    2. Load user roles using roles map utility
    3. Combine everything into UserSchema
    """

    # Async fetch
    user = await db.get(User, user_id)

    # User not found
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Await roles map (important)
    roles_map = await get_users_roles_map(user_id, db)

    # Safely extract roles
    user_roles = roles_map.get(user.id, [])

    # Return aggregated schema
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=user_roles,
        created_at=user.created_at
    )