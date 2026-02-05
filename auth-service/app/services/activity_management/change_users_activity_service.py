# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import User

from ...schemas.users.user_activity_schema import UserActivitySchema

# Change users activity
async def change_users_activity_status(
    user_ids: list[int],
    is_active: bool,
    db: Session
):
    # Get users
    users = db.exec(
        select(User).where(User.id.in_(user_ids))).all()

    if len(users) != len(user_ids):
        raise HTTPException(status_code=404, detail="User not found")

    # Change users activity
    for user in users:
        user.active = is_active

    db.commit()

    return [
        UserActivitySchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.active
        )
        for user in users
    ]