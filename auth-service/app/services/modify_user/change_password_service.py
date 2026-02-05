# Imports
from ...utils.get_user_with_role import get_user_with_role
from fastapi import HTTPException
from sqlmodel import Session
from ...models import User
from ..passwords.passwords_service import get_password_hash, verify_password

# Change password
async def change_user_password(
        user_id: int, 
        old_password: str | None, # google login nevajag paroli 
        new_password: str, 
        db: Session
    ):

    # Password validation
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")


    # Get user
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")
    
    # If old password is None, user is registered with Google
    if user.password_hash:
        # Parole ir iestatīta
        if not old_password or not verify_password(old_password, user.password_hash):
            raise HTTPException(status_code=403, detail="Invalid password")
        if old_password == new_password:
            raise HTTPException(status_code=400, detail="New password cannot be the same as the old password")
        
    else:
        # User is registered with Google
        if not user.email.endswith("@gmail.com"):
            raise HTTPException(status_code=403, detail="User is not registered with Google")


    # Change password
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)


    return await get_user_with_role(user_id, db)