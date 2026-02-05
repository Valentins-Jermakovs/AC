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
get_user_by_username_or_email(username_or_email: str, db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers:
   - Purpose: Retrieve users by partial match of username or email with pagination.
   - Input: search string, database session, page, limit.
   - Output: PaginatedUsers with matching users and pagination info.
   - Errors: 404 if no users match or page does not exist.
'''

# User by username or email
async def get_user_by_username_or_email(
    username_or_email: str, 
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    # Offset - pagination
    offset = (page - 1) * limit

    username_or_email = username_or_email.strip().lower()

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
        .where(
            or_(
                User.username.ilike(f"%{username_or_email}%"),
                User.email.ilike(f"%{username_or_email}%")
            )
        )
    ).all()

    if users == []:
        raise HTTPException(status_code=404, detail="User not found")
    
    total_users = len(users)

    # Check if page exists
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