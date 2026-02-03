# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User, Token
from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from ..services.password_service import verify_password
from ..services.token_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


"""
===== Auth Service =========================================================================

This module provides functionality for user authentication in the application.

Function: login_user
-------------------
Performs user login by verifying credentials and generating authentication tokens.

Parameters:
- db (Session): SQLModel database session for querying users and tokens.
- data (LoginSchema): Schema containing the username and password provided by the user.

Process:
1. Converts the username to lowercase for consistent lookup.
2. Checks if the user exists in the database. Raises HTTP 401 if not found.
3. Verifies the provided password against the stored password hash. Raises HTTP 401 if invalid.
4. Checks if the user is active. Raises HTTP 401 if inactive.
5. Deletes any existing refresh tokens for the user to ensure token rotation.
6. Generates a new refresh token and saves it in the database.
7. Generates a new access token containing the user's ID as the subject.
8. Returns a TokenWithRefreshSchema object containing:
   - access_token: JWT token for authenticating requests
   - token_type: always "bearer"
   - refresh_token: token used to obtain new access tokens

Raises:
- HTTPException with status code 401 if user not found, password is invalid, or user is inactive.
"""


# User login function
async def login_user(db: Session, data: LoginSchema) -> TokenWithRefreshSchema:

    data.username = data.username.lower()

    # User check in database
    user = db.exec(
        select(User).where(User.username == data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    if not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")


    # Tokens rotation
    token = db.exec(
        select(Token)
        .where(Token.user_id == user.id)
        .order_by(Token.created_at.desc())
    ).first()

    if token:
        db.delete(token)
        db.commit()


    # Generate new tokens
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)
    access_token = create_access_token({
        "sub": str(user.id)
    })

    # Return tokens
    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )
