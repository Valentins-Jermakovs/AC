# =========================
# User modification service
# =========================

from fastapi import HTTPException
from sqlmodel import Session, select
from ...models import User
from ...utils.get_user_with_role import get_user_with_role

# =========================
# Change user username
# =========================
async def change_user_username(
    user_id: int, 
    new_username: str, 
    db: Session
):
    """
    Changes a user's username.

    Validation and behavior:
    1. Load user by ID
       - Raises 404 if user not found
       - Raises 403 if user is inactive
    2. Normalize new username (strip & lowercase)
    3. Check if username already exists
       - Raises 400 if duplicate
    4. Update username in database
    5. Commit changes and refresh user object
    6. Return user data with roles

    :param user_id: ID of the user to update
    :param new_username: New username string
    :param db: Database session
    :return: UserSchema with updated username and roles
    :raises HTTPException: 404 if user not found, 403 if inactive, 400 if username exists
    """

    # Load user from database
    user = db.get(User, user_id)

    # Normalize new username
    new_username = new_username.strip().lower()

    # Validation: user existence
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validation: user active
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    # Validation: username uniqueness
    existing_user = db.exec(
        select(User).where(User.username == new_username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Update username
    user.username = new_username
    db.commit()
    db.refresh(user)

    # Return user data including roles
    return await get_user_with_role(user_id, db)