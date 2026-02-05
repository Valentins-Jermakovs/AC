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

    # Offset - pagination
    offset = (page - 1) * limit

    total_users = db.exec(
        select(User)
    ).all()

    total_users = len(total_users)

    # Check if page exists
    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # All users
    users = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .limit(limit)
        .offset(offset)
    ).all()

    # User -> UserSchema
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            active=user.active
        )
        for user in users
    ]

    # Meta
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )
    

    return PaginatedUsers(items=items, meta=meta)