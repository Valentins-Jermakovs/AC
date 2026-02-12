# =========================
# Remove role from users service
# =========================
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List
from ...models import User, Role, UserRole
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map

# =========================
# Remove a role from multiple users
# =========================
async def remove_role_from_users(
    user_ids: list[int],
    role_id: int,
    db: Session,
    user_id: str
) -> List[UserSchema]:
    """
    Removes a role from multiple users.

    Steps:
    1. Fetch users by IDs
       - Raise 404 if any user is not found
    2. Fetch role by role_id
       - Raise 404 if role does not exist
    3. For each user, delete the UserRole record if it exists
    4. Commit changes to database
    5. Map roles for updated users using get_users_roles_map
    6. Return list of UserSchema objects with updated roles

    :param user_ids: List of user IDs to remove role from
    :param role_id: ID of role to remove
    :param db: Database session
    :return: List of UserSchema objects with updated roles
    :raises HTTPException: 404 if user or role not found
    """

    # Fetch users
    users = db.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    if len(users) != len(set(user_ids)):
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )

    # check if current user try to modify his own role
    if int(user_id) in user_ids:
        raise HTTPException(
            status_code=403, 
            detail="You cannot modify your own role/roles"
        )

    # Fetch role
    role = db.exec(
        select(Role).where(Role.id == role_id)
    ).first()

    if not role:
        raise HTTPException(
            status_code=404, 
            detail="Role not found"
        )

    # Remove role from users
    for user in users:
        user_role = db.exec(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_id
            )
        ).first()

        if user_role:
            db.delete(user_role)

    # Commit all changes
    db.commit()

    # Map updated roles
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
