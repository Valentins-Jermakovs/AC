from sqlmodel import Session, select
from ..models import User, Role, UserRole
from typing import List

def get_users_roles_map(
    user_ids: list[int] | int,  # var būt int vai list[int]
    db: Session
) -> dict[int, list[str]]:

    # ja vienkāršs int, pārvērst sarakstā
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    elif not isinstance(user_ids, list):
        # drošības pārbaude
        user_ids = list(user_ids)

    if not user_ids:
        return {}

    rows = db.exec(
        select(User.id, Role.name)
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id.in_(user_ids))
    ).all()

    roles_map: dict[int, list[str]] = {}
    for user_id, role_name in rows:
        roles_map.setdefault(user_id, []).append(role_name)

    return roles_map

