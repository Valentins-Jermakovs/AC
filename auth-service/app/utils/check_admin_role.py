from fastapi import HTTPException, status
from sqlmodel import Session, select
from .check_access_token import check_access_token

from ..models import Role, UserRole

# check user to find admin privileges
async def check_admin_role(access_token: str, db: Session) -> int:
    user_id = await check_access_token(access_token)

    # try to find admin role
    user_roles = db.exec(
        select(UserRole).where(UserRole.user_id == user_id)
    ).all()

    for user_role in user_roles:
        role = db.exec(
            select(Role).where(Role.id == user_role.role_id)
        ).first()

        if role and role.name == "admin":
            return user_id

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin privileges required"
    )
    
