# Imports
from ..models import User, Role, UserRole
from sqlmodel import Session, select
from ..schemas.users.user_schema import UserSchema
from fastapi import HTTPException

# User with role by ID
async def get_user_with_role (
    user_id: int, 
    db: Session
):
    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        active=user.active
    )