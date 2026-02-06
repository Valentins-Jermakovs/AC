# =========================
# Admin role verification
# =========================

# FastAPI exceptions and HTTP status codes
from fastapi import HTTPException, status
# SQLModel session and select helper
from sqlmodel import Session, select
# Access token validation function
from .check_access_token import check_access_token
# Database models
from ..models import Role, UserRole

# =========================
# Admin access check
# =========================
async def check_admin_role(access_token: str, db: Session) -> int:
    """
    Checks whether the user has admin privileges.

    Steps:
    1. Validate access token and extract user ID
    2. Get all roles assigned to the user
    3. Check if any role is named "admin"

    :param access_token: JWT access token string
    :param db: database session
    :return: user_id if user has admin role
    :raises HTTPException: 403 if user is not an admin
    """

    # Validate token and get user ID
    user_id = await check_access_token(access_token)

    # Get all role links for this user
    user_roles = db.exec(
        select(UserRole).where(UserRole.user_id == user_id)
    ).all()

    # Check each assigned role
    for user_role in user_roles:
        # Get role details by role ID
        role = db.exec(
            select(Role).where(Role.id == user_role.role_id)
        ).first()

        # Admin role found -> access granted
        if role and role.name == "admin":
            return user_id

    # No admin role found -> access denied
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin privileges required"
    )
    
