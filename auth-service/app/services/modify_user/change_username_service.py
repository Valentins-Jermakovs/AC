# Imports
from ...utils.get_user_with_role import get_user_with_role
from fastapi import HTTPException
from sqlmodel import Session, select
from ...models import User

# Change username
async def change_user_username(
        user_id: int, 
        new_username: str, 
        db: Session
    ):

    # Users validation
    user = db.get(User, user_id)

    new_username = new_username.strip().lower()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    existing_user = db.exec(
        select(User).where(User.username == new_username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.username = new_username

    # Users data update
    db.commit()
    db.refresh(user)


    return await get_user_with_role(user_id, db)