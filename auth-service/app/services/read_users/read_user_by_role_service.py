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

    # Get users
    users = db.exec(
        select(User)
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(Role.name == role)
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="Role not found")

    total_users = len(users)
    offset = (page - 1) * limit

    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # Get users roles
    user_ids = [user.id for user in users]
    roles_map = get_users_roles_map(user_ids, db)

    # Convert UserSchema
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