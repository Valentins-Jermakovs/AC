# =========================
# User search service
# =========================

from sqlmodel import Session, select
from sqlalchemy import or_
from fastapi import HTTPException
from ...models import User
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Search users by username or email
# =========================
async def get_user_by_username_or_email(
    username_or_email: str, 
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:
    """
    Searches users by partial match of username or email with pagination.

    Steps:
    1. Normalize search string (strip & lowercase)
    2. Fetch all users matching username or email (case-insensitive)
       - Raise 404 if no users found
    3. Calculate pagination offset
       - Raise 404 if page exceeds total users
    4. Fetch user IDs for role mapping
    5. Map roles using get_users_roles_map
    6. Build list of UserSchema objects with roles
    7. Create pagination metadata
    8. Return PaginatedUsers with items and meta

    :param username_or_email: Partial username or email to search
    :param db: Database session
    :param page: Page number (default 1)
    :param limit: Users per page (default 10)
    :return: PaginatedUsers object with matching users and pagination metadata
    :raises HTTPException: 404 if no users match or page is invalid
    """

    # Pagination offset
    offset = (page - 1) * limit
    username_or_email = username_or_email.strip().lower()

    # Fetch all matching users
    users = db.exec(
        select(User).where(
            or_(
                User.username.ilike(f"%{username_or_email}%"),
                User.email.ilike(f"%{username_or_email}%")
            )
        )
    ).all()

    # No users found
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    total_users = len(users)

    # Check if page exists
    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # Map users to their roles
    user_ids = [user.id for user in users]
    roles_map = get_users_roles_map(user_ids, db)

    # Build paginated UserSchema list
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

    # Pagination metadata
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)