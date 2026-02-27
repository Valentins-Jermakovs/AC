# =========================
# User search service (ASYNC FIXED)
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlalchemy import or_
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
# Models
from ...models import UserModel
# Schemas
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsersSchema, PaginationMeta
# Utils
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Search users by username or email
# =========================
async def get_user_by_username_or_email(
    username_or_email: str,
    db: AsyncSession,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsersSchema:

    offset = (page - 1) * limit
    search = username_or_email.strip().lower()

    # ASYNC QUERY — WAIT FOR IT
    result = await db.exec(
        select(UserModel).where(
            or_(
                UserModel.username.ilike(f"%{search}%"),
                UserModel.email.ilike(f"%{search}%")
            )
        )
    )

    # NOW get all results
    users = result.all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    total_users = len(users)

    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # IDs
    user_ids = [user.id for user in users]

    # ASYNC roles map
    roles_map = await get_users_roles_map(user_ids, db)

    # Paginated slice
    paginated_users = users[offset:offset + limit]

    items = [
        UserSchema(
            id=user.id,
            username=user.username or "",
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, []),
            created_at=user.created_at
        )
        for user in paginated_users
    ]

    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsersSchema(items=items, meta=meta)