# =========================
# User listing by role service (ASYNC FIXED)
# =========================

# Imports
# Libraries
from sqlmodel import select
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select as sa_select
# Models
from ...models import UserModel, RoleModel, UserRoleModel
# Schemas
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsersSchema, PaginationMeta
# Utils
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get users by role with pagination
# =========================
async def get_users_by_role(
    role: str,
    db: AsyncSession,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsersSchema:

    role = role.strip().lower()
    offset = (page - 1) * limit

    # ASYNC QUERY — IMPORTANT: await
    result = await db.exec(
        select(UserModel)
        .join(UserRoleModel, UserRoleModel.user_id == UserModel.id)
        .join(RoleModel, RoleModel.id == UserRoleModel.role_id)
        .where(RoleModel.name == role)
    )

    users = result.all()

    if not users:
        raise HTTPException(status_code=404, detail="Role not found")

    total_users = len(users)

    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # Roles async
    user_ids = [user.id for user in users]
    roles_map = await get_users_roles_map(user_ids, db)

    paginated = users[offset:offset + limit]

    items = [
        UserSchema(
            id=user.id,
            username=user.username or "",
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, []),
            created_at=user.created_at
        )
        for user in paginated
    ]

    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsersSchema(items=items, meta=meta)