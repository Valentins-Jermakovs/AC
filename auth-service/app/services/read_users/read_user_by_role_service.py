# Imports
from sqlmodel import Session, select
from sqlalchemy import or_
from fastapi import HTTPException
from ...models import (
    User, 
    Role, 
    UserRole
)
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta

'''
get_users_by_role(role: str, db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers:
   - Purpose: Retrieve users filtered by role with pagination.
   - Input: role name, database session, page, limit.
   - Output: PaginatedUsers with users of specified role and pagination info.
   - Errors: 404 if no users with the role exist or page does not exist.
'''

# Users by role
async def get_users_by_role(
    role: str, 
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    role = role.strip().lower()

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
        .where(Role.name == role)
    ).all()

    if users == []:
        raise HTTPException(status_code=404, detail="Role not found")
    
    total_users = len(users)

    # Check if page exists
    offset = (page - 1) * limit
    if offset >= len(users):
        raise HTTPException(status_code=404, detail="Page not found")
    
    # User -> UserSchema
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            active=user.active
        )
        for user in users[offset:offset + limit]
    ]

    # Meta
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)