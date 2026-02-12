# =========================
# User password change service
# =========================

from fastapi import HTTPException
from sqlmodel import Session
from ...models import User
from ...utils.get_user_with_role import get_user_with_role
from ..passwords.passwords_service import get_password_hash, verify_password


# =========================
# Change user password
# =========================
async def change_user_password(
    user_id: int, 
    old_password: str | None, # None if Google login user 
    new_password: str, 
    db: Session
):
    """
    Changes a user's password.

    Steps:
    1. Validate new password length (minimum 8 characters)
    2. Load user by ID
       - Raises 404 if not found
       - Raises 403 if inactive
    3. Determine user type:
       - Local user: must provide correct old password
       - Google user: old_password can be None
    4. Prevent new password being same as old password
    5. Hash new password and update in database
    6. Commit changes and refresh user object
    7. Return user data with roles

    :param user_id: ID of the user to update
    :param old_password: Current password for verification (optional for Google login users)
    :param new_password: New password
    :param db: Database session
    :return: UserSchema with updated user data and roles
    :raises HTTPException:
        - 400 if new password is too short or same as old
        - 403 if old password invalid or user not eligible
        - 404 if user not found
    """

    # Validate new password length
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Local user with password set
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")
    
    # Local login
    if user.password_hash:

        if not old_password or not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=403, 
                detail="Invalid password"
            )
        
        if verify_password(new_password, user.password_hash):
            raise HTTPException(
                status_code=400, 
                detail="New password cannot be the same as the old password"
            )

    # Update password
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)

    # Return updated user with roles
    return await get_user_with_role(user_id, db)