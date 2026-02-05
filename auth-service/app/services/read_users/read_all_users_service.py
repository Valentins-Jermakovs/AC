# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import (
    User, 
    Role, 
    UserRole
)
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta
from ...utils.get_users_roles_map import get_users_roles_map

'''
Function:

get_users_paginated(db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers:
    - Purpose: Retrieve all users with pagination.
    - Input: database session, page number, limit per page.
    - Output: PaginatedUsers object containing list of UserSchema and pagination metadata.
    - Errors: 404 if requested page does not exist.
'''

# All users paginated
async def get_users_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    # Pagination offset
    offset = (page - 1) * limit

    # Total users
    total_users = db.exec(select(User)).all()
    total_count = len(total_users)

    # Check if page exists
    if offset >= total_count:
        raise HTTPException(status_code=404, detail="Page not found")

    # Paginated users
    users_page = db.exec(
        select(User)
        .limit(limit)
        .offset(offset)
    ).all()

    # Create list of user ids
    user_ids = [user.id for user in users_page]

    # Get users roles
    roles_map = get_users_roles_map(user_ids, db)

    # Create list of user schemas
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, [])
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