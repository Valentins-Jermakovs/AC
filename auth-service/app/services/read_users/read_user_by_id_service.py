# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ...models import (
    User, 
    Role, 
    UserRole
)
from ...schemas.users.user_schema import UserSchema
from ...utils.get_users_roles_map import get_users_roles_map

'''
get_user_by_id(user_id: int, db: Session) -> UserSchema:
   - Purpose: Retrieve a single user by ID.
   - Input: user ID, database session.
   - Output: UserSchema object with user info and role.
   - Errors: 404 if user not found.
'''

# User by ID
async def get_user_by_id(
    user_id: int, 
    db: Session
) -> UserSchema:

    # Atlasām lietotāju
    user = db.exec(
        select(User).where(User.id == user_id)
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Iegūstam visas lomas kā list
    roles_map = get_users_roles_map(user_id, db)
    user_roles = roles_map.get(user.id, [])

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        active=user.active,
        roles=user_roles  # ← pareizi Pydantic schemai
    )