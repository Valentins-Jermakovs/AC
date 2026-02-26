# =========================
# Remove role from users service
# =========================

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List

from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Remove a role from multiple users
# =========================
async def remove_role_from_users(
    user_ids: list[int],
    role_id: int,
    db: AsyncSession,
    user_id: str
) -> List[UserSchema]:
    """
    Removes a role from multiple users.
    """

    # =========================
    # Fetch users async
    # =========================
    result_users = await db.exec(
        select(User).where(User.id.in_(user_ids))
    )

    users = result_users.all()

    if len(users) != len(set(user_ids)):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent self role modification
    if int(user_id) in user_ids:
        raise HTTPException(
            status_code=403,
            detail="You cannot modify your own role/roles"
        )

    # =========================
    # Fetch role async
    # =========================
    result_role = await db.exec(
        select(Role).where(Role.id == role_id)
    )

    role = result_role.first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # =========================
    # Remove role from users
    # =========================
    for user in users:

        result_user_role = await db.exec(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_id
            )
        )

        user_role = result_user_role.first()

        if user_role:
            await db.delete(user_role)

    # =========================
    # Commit async
    # =========================
    await db.commit()

    # =========================
    # Reload roles
    # =========================
    roles_map = await get_users_roles_map(user_ids, db)

    return [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, []),
            created_at=user.created_at
        )
        for user in users
    ]