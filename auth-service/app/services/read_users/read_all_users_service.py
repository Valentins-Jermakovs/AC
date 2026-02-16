# =========================
# User listing with pagination
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get paginated users
# =========================
async def get_users_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:
    """
    Retrieves users with pagination and includes their roles.

    Steps:
    1. Calculate pagination offset
    2. Count total users
    3. Raise 404 if requested page exceeds total users
    4. Fetch users for current page using limit & offset
    5. Build list of user IDs
    6. Fetch roles for these users
    7. Build list of UserSchema objects including roles
    8. Build pagination metadata
    9. Return PaginatedUsers object containing users and meta

    :param db: Database session
    :param page: Page number (default 1)
    :param limit: Number of users per page (default 10)
    :return: PaginatedUsers object with list of UserSchema and metadata
    :raises HTTPException: 404 if requested page does not exist
    """

    # Pagination offset
    offset = (page - 1) * limit

    # Total users count
    total_users = db.exec(select(User)).all()
    total_count = len(total_users)

    # Check if page exists
    if offset >= total_count:
        raise HTTPException(status_code=404, detail="Page not found")

    # Fetch paginated users
    users_page = db.exec(
        select(User)
        .limit(limit)
        .offset(offset)
    ).all()

    # List of user IDs
    user_ids = [user.id for user in users_page]

    # Map users to their roles
    roles_map = get_users_roles_map(user_ids, db)

    # Build list of UserSchema objects
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

    # Pagination metadata
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_count,
        total_pages=(total_count + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)