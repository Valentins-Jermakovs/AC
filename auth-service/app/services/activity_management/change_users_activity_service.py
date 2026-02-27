# =========================
# User activity service
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
# Models
from ...models import UserModel
# Schemas
from ...schemas.users.user_activity_schema import UserActivitySchema


# =========================
# Change users activity status
# =========================
async def change_users_activity_status(
    user_ids: list[int],
    is_active: bool,
    db: AsyncSession,
    user_id: str
):
    """
    Changes activity status for multiple users.
    """

    # =========================
    # Load users async
    # =========================
    result = await db.exec(
        select(UserModel).where(UserModel.id.in_(user_ids))
    )

    users = result.all()

    # If some users were not found
    if len(users) != len(user_ids):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent user from disabling himself
    if int(user_id) in [user.id for user in users]:
        raise HTTPException(
            status_code=403,
            detail="You cannot change your own activity status"
        )

    # =========================
    # Update users
    # =========================
    for user in users:
        user.active = is_active

    # Async commit
    await db.commit()

    # =========================
    # Build response
    # =========================
    return [
        UserActivitySchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.active
        )
        for user in users
    ]