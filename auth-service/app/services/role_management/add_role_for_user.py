# =========================
# Add role for users service
# =========================

# Imports
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List
# Models
from ...models import UserModel, RoleModel, UserRoleModel
# Schemas
from ...schemas.users.user_schema import UserSchema
# Utils
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Add a role to multiple users
# =========================
async def add_role_for_users(
    user_ids: list[int],
    role_id: int,
    db: AsyncSession,
    user_id: str
) -> List[UserSchema]:
    """
    Adds a role to multiple users.
    """

    # =========================
    # Fetch users async
    # =========================
    result_users = await db.exec(
        select(UserModel).where(UserModel.id.in_(user_ids))
    )

    users = result_users.all()

    if len(users) != len(set(user_ids)):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent self-role modification
    if int(user_id) in user_ids:
        raise HTTPException(
            status_code=403,
            detail="You cannot modify your own role/roles"
        )

    # =========================
    # Fetch role async
    # =========================
    result_role = await db.exec(
        select(RoleModel).where(RoleModel.id == role_id)
    )

    role = result_role.first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # =========================
    # Assign role (avoid duplicates)
    # =========================
    for user in users:

        result_existing = await db.exec(
            select(UserRoleModel).where(
                UserRoleModel.user_id == user.id,
                UserRoleModel.role_id == role_id
            )
        )

        exists = result_existing.first()

        if not exists:
            db.add(
                UserRoleModel(
                    user_id=user.id,
                    role_id=role_id
                )
            )

    # =========================
    # Commit async
    # =========================
    await db.commit()

    # =========================
    # Reload roles map
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