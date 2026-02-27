# =========================
# User modification service
# =========================

# Imports
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
# Dependencies
from ..dependencies.data_base_connection import get_db
# Services
from ..services.modify_user.change_email_service import change_user_email
from ..services.modify_user.change_password_service import change_user_password
from ..services.modify_user.change_username_service import change_user_username
from ..services.tokens_management.refresh_tokens_service import check_access_token
# Schemas
from ..schemas.users.user_schema import UserSchema
from ..schemas.users.change_username_schema import ChangeUsernameSchema
from ..schemas.users.change_email_schema import ChangeEmailSchema
from ..schemas.users.change_password_schema import ChangePasswordSchema


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/modifications",    # All endpoints start with /modifications
    tags=["User modification service"]  # Tag for docs grouping
)

# Security scheme for extracting access token
security = HTTPBearer()

# =========================
# Change username endpoint
# =========================
@router.put(
    "/username/", 
    response_model=UserSchema,
    summary="Change user username",
)
async def modify_username(
    data: ChangeUsernameSchema, # New username from request body
    db: Annotated[Session, Depends(get_db)],    # Database session
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
):
    """
    Update user's username.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to change username in DB
    4. Return updated user
    """
    access_token = credentials.credentials

    # Verify access token
    user_id = await check_access_token(access_token)
    
    # Update username
    user = await change_user_username(
        user_id=user_id, 
        new_username=data.new_username, 
        db=db
    )

    return user


# =========================
# Change email endpoint
# =========================
@router.put(
        "/email/", 
        response_model=UserSchema,
        summary="Change user email",
    )
async def modify_email_endpoint(
    data: ChangeEmailSchema,    # New email from request body
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
):
    """
    Update user's email.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to change email in DB
    4. Return updated user
    """
    access_token = credentials.credentials

    # Verify access token
    user_id = await check_access_token(access_token)

    # Update email
    user = await change_user_email(
        user_id=user_id, 
        new_email=data.new_email, 
        db=db
    )

    return user


# =========================
# Change password endpoint
# =========================
@router.put(
        "/password/", 
        response_model=UserSchema,
        summary="Change user password",
    )
async def change_password_endpoint(
    data: ChangePasswordSchema, # Old and new password from request body
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
):
    """
    Update user's password.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to change password in DB (verify old password)
    4. Return updated user
    """
    access_token = credentials.credentials

    # Verify access token
    user_id = await check_access_token(access_token)

    # Update password
    user = await change_user_password(
        user_id=user_id, 
        old_password=data.old_password, 
        new_password=data.new_password, 
        db=db
    )

    return user