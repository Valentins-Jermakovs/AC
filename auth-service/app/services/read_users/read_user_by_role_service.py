# =========================
# User listing by role service
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...schemas.users.pagination_schema import PaginatedUsers, PaginationMeta
from ...utils.get_users_roles_map import get_users_roles_map


# =========================
# Get users by role with pagination
# =========================
async def get_users_by_role(
    role: str,
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:
    """
    Retrieves users filtered by a specific role with pagination.

    Steps:
    1. Normalize role string (strip & lowercase)
    2. Fetch all users assigned to the role
       - Raise 404 if no users found
    3. Calculate pagination offset
       - Raise 404 if page exceeds total users
    4. Map roles for these users using get_users_roles_map
    5. Build list of UserSchema objects with roles
    6. Build pagination metadata
    7. Return PaginatedUsers with items and meta

    :param role: Role name to filter users
    :param db: Database session
    :param page: Page number (default 1)
    :param limit: Users per page (default 10)
    :return: PaginatedUsers object with users of specified role and metadata
    :raises HTTPException: 404 if role not found or page is invalid
    """

    # Normalize role
    role = role.strip().lower()

    # Fetch users with given role
    users = db.exec(
        select(User)
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(Role.name == role)
    ).all()

    # No users found for this role
    if not users:
        raise HTTPException(status_code=404, detail="Role not found")

    total_users = len(users)
    offset = (page - 1) * limit

    # Pagination check
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
            roles=roles_map.get(user.id, []),
            created_at=user.created_at
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