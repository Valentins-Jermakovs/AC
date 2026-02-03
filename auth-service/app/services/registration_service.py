# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User, Role, UserRole
from ..schemas.registration_schema import RegistrationSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from .password_service import get_password_hash
from .token_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


"""
===== User Registration Service =========================================================

Function: register_user
-----------------------
Registers a new user in the system and generates authentication tokens.

Parameters:
- data (RegistrationSchema): User registration data including username, email, and password.
- db (Session): SQLModel database session for querying and modifying user and role data.

Process:
1. Converts username and email to lowercase for consistency.
2. Checks if the username or email already exists. Raises HTTP 400 if either exists.
3. Creates a new user with a hashed password and saves it to the database.
4. Assigns the user to the default "user" role if it exists.
5. Generates an access token and a refresh token for the new user.
6. Saves the refresh token in the database.
7. Returns a TokenWithRefreshSchema object containing:
   - access_token: JWT token for authenticating requests
   - token_type: always "bearer"
   - refresh_token: token used to obtain new access tokens

Raises:
- HTTPException with status code 400 if the username or email already exists.
"""


# User registration function
async def register_user(
    data: RegistrationSchema,
    db: Session
) -> TokenWithRefreshSchema:

    data.username = data.username.lower()
    data.email = data.email.lower()

    # Check if user already exists
    existing_user = db.exec(select(User).where(User.username == data.username)).first()
    existing_email = db.exec(select(User).where(User.email == data.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # New user registration
    user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password)
    )

    db.add(user)        
    db.commit()         
    db.refresh(user)    

    # Add user to "user" role
    user_role = db.exec(
        select(Role).where(Role.name == "user")
    ).first()

    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()

    # Create tokens
    access_token = create_access_token({
        "sub": str(user.id)
    })
    refresh_token = create_refresh_token()
    save_refresh_token(
        refresh_token, 
        user.id, 
        db
    )

    # Return tokens
    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )
