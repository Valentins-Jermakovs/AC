# =========================
# User roles mapping utility
# =========================

from sqlmodel import Session, select
from typing import List
# Database models
from ..models import User, Role, UserRole


# =========================
# Build user → roles map
# =========================
def get_users_roles_map(
    user_ids: list[int] | int,  # can be a single user ID or list of IDs
    db: Session
) -> dict[int, list[str]]:
    """
    Builds a mapping of users to their role names.

    This function is optimized to load roles for multiple users
    in a single database query.

    Example return value:
    {
        1: ["admin", "editor"],
        2: ["user"]
    }

    :param user_ids: user ID or list of user IDs
    :param db: database session
    :return: dictionary mapping user_id -> list of role names
    """

    # # If a single ID is passed, convert it to a list
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    
    # Safety check: try to convert other iterables to list
    elif not isinstance(user_ids, list):
        user_ids = list(user_ids)

    # No users provided -> return empty result
    if not user_ids:
        return {}

    # Query all roles for given users in one SQL call
    rows = db.exec(
        select(User.id, Role.name)
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id.in_(user_ids))
    ).all()

    # Build result map: user_id -> [role_name, ...]
    roles_map: dict[int, list[str]] = {}
    
    for user_id, role_name in rows:
        roles_map.setdefault(user_id, []).append(role_name)

    return roles_map

