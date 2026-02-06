# =========================
# User modification service
# =========================

from fastapi import HTTPException
from sqlmodel import Session, select
from ...models import User
from ...utils.get_user_with_role import get_user_with_role


# =========================
# Change user email
# =========================
async def change_user_email(
    user_id: int, 
    new_email: str, 
    db: Session
):
    """
    Changes a user's email address.

    Steps:
    1. Load user by ID
       - Raises 404 if not found
       - Raises 403 if user is inactive
    2. Normalize new email (strip & lowercase)
    3. Check if new email already exists
       - Raises 400 if duplicate
    4. Update email in database
    5. Commit changes and refresh user object
    6. Return user data with roles

    :param user_id: ID of the user to update
    :param new_email: New email address
    :param db: Database session
    :return: UserSchema with updated email and roles
    :raises HTTPException: 404 if user not found, 403 if inactive, 400 if email exists
    """

    # Load user from database
    user = db.get(User, user_id)

    # Normalize new email
    new_email = new_email.strip().lower()

    # Validation: user existence
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validation: user active
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    # Validation: email uniqueness
    existing_user = db.exec(select(User).where(User.email == new_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Update user email
    user.email = new_email
    db.commit()
    db.refresh(user)

    # Return user data including roles
    return await get_user_with_role(user_id, db)