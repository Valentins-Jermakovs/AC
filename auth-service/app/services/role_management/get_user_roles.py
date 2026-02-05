from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map

async def get_user_roles(
    user_id: int,
    db: Session
) -> UserSchema:

    user = db.exec(
        select(User).where(User.id == user_id)
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    roles_map = get_users_roles_map(user_id, db)

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=roles_map.get(user_id, [])
    )
