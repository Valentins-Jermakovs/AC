# =========================
# User roles mapping utility (ASYNC)
# =========================

# Imports
# Libraries
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
# Database models
from ..models import UserModel, RoleModel, UserRoleModel


# =========================
# Build user -> roles map
# =========================
async def get_users_roles_map(
    user_ids: list[int] | int,
    db: AsyncSession
) -> dict[int, list[str]]:
    """
    Builds a mapping of users to their role names.
    Async safe.
    """

    # If single id -> convert to list
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    elif not isinstance(user_ids, list):
        user_ids = list(user_ids)

    if not user_ids:
        return {}

    # =========================
    # Query in ONE async call
    # =========================
    result = await db.exec(
        select(UserModel.id, RoleModel.name)
        .join(UserRoleModel, UserRoleModel.user_id == UserModel.id)
        .join(RoleModel, RoleModel.id == UserRoleModel.role_id)
        .where(UserModel.id.in_(user_ids))
    )

    rows = result.all()

    roles_map: dict[int, list[str]] = {}

    for user_id, role_name in rows:
        roles_map.setdefault(user_id, []).append(role_name)

    return roles_map