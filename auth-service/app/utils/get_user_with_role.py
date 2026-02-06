# =========================
# User data aggregation
# =========================

from sqlmodel import Session
from fastapi import HTTPException
# Database model
from ..models import User
# Response schema (what API returns)
from ..schemas.users.user_schema import UserSchema
# Utility that maps users to their roles
from .get_users_roles_map import get_users_roles_map


# =========================
# Get user with roles
# =========================
async def get_user_with_role(user_id: int, db: Session) -> UserSchema:
    """
    Returns user data together with assigned roles.

    Steps:
    1. Load user from database
    2. Load user roles using roles map utility
    3. Combine everything into UserSchema

    :param user_id: ID of the user
    :param db: database session
    :return: UserSchema with roles included
    :raises HTTPException: 404 if user does not exist
    """

    # Get user by ID
    user = db.get(User, user_id)

    # User not found -> return 404
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )

    # Get roles for this user
    # get_users_roles_map returns: { user_id: [role_name, ...] }
    roles_map = get_users_roles_map(user_id, db)

    # Extract roles for current user
    user_roles = roles_map.get(user.id, [])

    # Build response schema
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=user_roles  # roles must always be included in response
    )
