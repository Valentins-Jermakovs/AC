# =========================
# User password change service
# =========================

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ...models import User
from ...utils.get_user_with_role import get_user_with_role
from ..passwords.passwords_service import get_password_hash, verify_password


# =========================
# Change user password
# =========================
async def change_user_password(
    user_id: int,
    old_password: str | None,
    new_password: str,
    db: AsyncSession
):
    """
    Changes a user's password.
    """

    # Validate new password length
    if len(new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    # Load user async
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )

    # =========================
    # Local user validation
    # =========================
    if user.password_hash:

        # Check old password
        if not old_password or not await verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=403,
                detail="Invalid password"
            )

        # Prevent using same password
        if await verify_password(new_password, user.password_hash):
            raise HTTPException(
                status_code=400,
                detail="New password cannot be the same as the old password"
            )

    # =========================
    # Update password
    # =========================
    user.password_hash = await get_password_hash(new_password)

    # Async commit
    await db.commit()

    # Async refresh
    await db.refresh(user)

    # Return updated user with roles
    return await get_user_with_role(user_id, db)