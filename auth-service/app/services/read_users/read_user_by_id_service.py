# =========================
# User retrieval service
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get user by ID
# =========================
async def get_user_by_id(
    user_id: int, 
    db: Session
) -> UserSchema:
    """
    Retrieves a single user by ID and includes their roles.

    Steps:
    1. Fetch user from database by ID
       - Raises 404 if user not found
    2. Fetch user's roles using get_users_roles_map
    3. Return a UserSchema object containing user info and roles

    :param user_id: ID of the user to retrieve
    :param db: Database session
    :return: UserSchema with user details and roles
    :raises HTTPException: 404 if user not found
    """

    # Fetch user
    user = db.exec(
        select(User).where(User.id == user_id)
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's roles
    roles_map = get_users_roles_map(user_id, db)
    user_roles = roles_map.get(user.id, [])

    # If user username is None, set it to empty string
    if user.username is None:
        user.username = ""

    # created_at to year, month, day
    user.created_at = user.created_at.strftime("%Y-%m-%d")

    # Return user schema with roles
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=user_roles,
        created_at=user.created_at
    )