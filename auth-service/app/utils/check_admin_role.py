# =========================
# Admin role verification
# =========================

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .check_access_token import check_access_token
from ..models import Role, UserRole


# =========================
# Admin access check
# =========================
async def check_admin_role(access_token: str, db: AsyncSession) -> str:
    """
    Validates whether user has admin role.
    Returns user_id if OK.
    Raises 403 otherwise.
    """

    # Validate token
    user_id = await check_access_token(access_token)

    # Get all user roles (ASYNC -> MUST await)
    result = await db.exec(
        select(UserRole).where(UserRole.user_id == user_id)
    )

    user_roles = result.all()

    # If no roles -> deny
    if not user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    # Check if any role is admin
    for user_role in user_roles:

        role_result = await db.exec(
            select(Role).where(Role.id == user_role.role_id)
        )

        role = role_result.first()

        if role and role.name == "admin":
            return user_id

    # No admin found
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin privileges required"
    )