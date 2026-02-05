from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map
from typing import List
# Remove role from users
async def remove_role_from_users(
    user_ids: list[int],
    role_id: int,
    db: Session
) -> List[UserSchema]:

    users = db.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    if len(users) != len(set(user_ids)):
        raise HTTPException(404, "User not found")

    role = db.exec(
        select(Role).where(Role.id == role_id)
    ).first()

    if not role:
        raise HTTPException(404, "Role not found")

    for user in users:
        user_role = db.exec(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_id
            )
        ).first()

        if user_role:
            db.delete(user_role)

    db.commit()

    roles_map = get_users_roles_map(user_ids, db)

    return [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, [])
        )
        for user in users
    ]
