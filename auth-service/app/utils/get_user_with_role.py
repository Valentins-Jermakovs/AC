from sqlmodel import Session
from fastapi import HTTPException
from ..models import User
from ..schemas.users.user_schema import UserSchema
from .get_users_roles_map import get_users_roles_map

async def get_user_with_role(user_id: int, db: Session) -> UserSchema:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Iegūstam lomas šim lietotājam
    roles_map = get_users_roles_map(user_id, db)  # var nodot vienu int
    user_roles = roles_map.get(user.id, [])

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=user_roles  # obligāti jābūt šeit
    )
