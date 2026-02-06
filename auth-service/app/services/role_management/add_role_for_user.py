# =========================
# Add role for users service
# =========================
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List
from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map

# =========================
# Add a role to multiple users
# =========================
async def add_role_for_users(
    user_ids: list[int],
    role_id: int,
    db: Session
) -> List[UserSchema]:
    """
    Adds a role to multiple users.

    Steps:
    1. Fetch users by IDs
       - Raise 404 if any user is not found
    2. Fetch role by role_id
       - Raise 404 if role does not exist
    3. Check for existing user-role assignments to avoid duplicates
       - Only add if the user does not already have the role
    4. Commit changes to database
    5. Map roles for updated users using get_users_roles_map
    6. Return list of UserSchema objects with updated roles

    :param user_ids: List of user IDs to assign role
    :param role_id: ID of role to assign
    :param db: Database session
    :return: List of UserSchema objects with updated roles
    :raises HTTPException: 404 if user or role not found
    """

    # Fetch users
    users = db.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    if len(users) != len(set(user_ids)):
        raise HTTPException(404, "User not found")

    # Fetch role
    role = db.exec(
        select(Role).where(Role.id == role_id)
    ).first()

    if not role:
        raise HTTPException(404, "Role not found")

    # Assign role to users if not already assigned
    for user in users:
        exists = db.exec(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_id
            )
        ).first()

        if not exists:
            db.add(UserRole(
                user_id=user.id,
                role_id=role_id
            ))

    # Commit all changes
    db.commit()

    # Map roles for updated users
    roles_map = get_users_roles_map(user_ids, db)

    # Return updated user schemas
    return [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            active=user.active,
            roles=roles_map.get(user.id, [])
        )
        for user in users
    ]
