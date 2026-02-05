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
from ...utils.get_users_roles_map import get_users_roles_map

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

    offset = (page - 1) * limit
    username_or_email = username_or_email.strip().lower()

    # Get users
    users = db.exec(
        select(User).where(
            or_(
                User.username.ilike(f"%{username_or_email}%"),
                User.email.ilike(f"%{username_or_email}%")
            )
        )
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    total_users = len(users)

    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # Get users roles
    user_ids = [user.id for user in users]
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