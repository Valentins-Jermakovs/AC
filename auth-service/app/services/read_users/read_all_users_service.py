# =========================
# User listing with pagination (ASYNC FIXED)
# =========================

from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from ...models import User
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get paginated users
# =========================
async def get_users_paginated(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:
    """
    Retrieves users with pagination and includes their roles.
    Async-safe version.
    """

    # Pagination offset
    offset = (page - 1) * limit

    # =========================
    # Count total users (optimized)
    # =========================
    total_count = (await db.exec(
        select(func.count(User.id))
    )).one()

    # Check if page exists
    if offset >= total_count and total_count != 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # =========================
    # Fetch paginated users
    # =========================
    result = await db.exec(
        select(User)
        .limit(limit)
        .offset(offset)
    )
    users_page = result.all()

    # If no users found
    if not users_page:
        return PaginatedUsers(
            items=[],
            meta=PaginationMeta(
                page=page,
                limit=limit,
                total_users=total_count,
                total_pages=(total_count + limit - 1) // limit
            )
        )

    # =========================
    # Extract user IDs
    # =========================
    user_ids = [user.id for user in users_page]

    # =========================
    # Fetch roles mapping
    # =========================
    roles_map = await get_users_roles_map(user_ids, db)

    # =========================
    # Build response items
    # =========================
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, []),
            created_at=user.created_at
        )
        for user in users_page
    ]

    # =========================
    # Pagination metadata
    # =========================
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_count,
        total_pages=(total_count + limit - 1) // limit
    )

    return PaginatedUsers(
        items=items,
        meta=meta
    )