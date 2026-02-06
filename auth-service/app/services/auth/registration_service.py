# =========================
# User registration service
# =========================

from sqlmodel import Session, select
from fastapi import HTTPException
# Database models
from ...models import User, Role, UserRole
# Schemas
from ...schemas.auth.registration_schema import RegistrationSchema
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema
# Password hashing utility
from ..passwords.passwords_service import get_password_hash
# Token management utilities
from ..tokens_management.create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)



# =========================
# Register new user
# =========================
async def register_user(
    data: RegistrationSchema,
    db: Session
) -> TokenRefreshSchema:
    """
    Registers a new user and generates authentication tokens.

    Steps:
    1. Normalize username and email to lowercase
    2. Check if username or email already exists
       - Raises 400 if either exists
    3. Create new user with hashed password
    4. Assign default "user" role if it exists
    5. Generate access and refresh tokens
    6. Save refresh token in database
    7. Return tokens in TokenRefreshSchema

    :param data: RegistrationSchema containing username, email, and password
    :param db: SQLModel database session
    :return: TokenRefreshSchema containing access_token, token_type, refresh_token
    :raises HTTPException: 400 if username or email already exists
    """

    # Normalize inputs
    data.username = data.username.lower()
    data.email = data.email.lower()

    # Check if username or email already exists
    existing_user = db.exec(select(User).where(User.username == data.username)).first()
    existing_email = db.exec(select(User).where(User.email == data.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create new user with hashed password
    user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password)
    )

    db.add(user)        
    db.commit()         
    db.refresh(user)    

    # Assign default "user" role if exists
    user_role = db.exec(
        select(Role).where(Role.name == "user")
    ).first()

    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()

    # Generate access and refresh tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token()
    save_refresh_token(refresh_token, user.id, db)

    # Return tokens to client
    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )