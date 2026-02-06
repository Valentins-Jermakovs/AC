# =========================
# User activity service
# =========================

# SQLModel imports
from sqlmodel import Session, select
# FastAPI exception
from fastapi import HTTPException
# Database model
from ...models import User
# Response schema
from ...schemas.users.user_activity_schema import UserActivitySchema


# =========================
# Change users activity status
# =========================
async def change_users_activity_status(
    user_ids: list[int],
    is_active: bool,
    db: Session
):
    """
    Changes activity status for multiple users.

    Behavior:
    - Loads users by provided IDs
    - Verifies that all users exist
    - Updates `active` field for each user
    - Returns updated user activity data

    :param user_ids: list of user IDs to update
    :param is_active: new activity status (True / False)
    :param db: database session
    :return: list of UserActivitySchema objects
    """


    # Load users from database
    users = db.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    # If some users were not found, return 404
    if len(users) != len(user_ids):
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )

    # Update activity status for each user
    for user in users:
        user.active = is_active

    # Save changes to database
    db.commit()

    # Build response
    return [
        UserActivitySchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.active
        )
        for user in users
    ]