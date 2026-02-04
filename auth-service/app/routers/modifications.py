# Imports
from fastapi import (
    APIRouter, 
    Depends,
    Query,
    Header
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from ..schemas.user_schema import UserSchema
from ..schemas.change_password_schema import ChangePasswordSchema
from ..schemas.change_email_schema import ChangeEmailSchema
from ..schemas.change_username_schema import ChangeUsernameSchema
from ..services.user_modification_service import (
    change_user_username, 
    change_user_email, 
    change_user_password
)
from ..services.refresh_tokens_service import (
    refresh_access_token, 
    get_user_id_from_access_token
)
from ..dependencies.data_base_connection import get_db

# Router
router = APIRouter(
    prefix="/modifications", 
    tags=["Modifications"]
)

security = HTTPBearer()

# Change username
@router.put(
    "/username/", 
    response_model=UserSchema,
    summary="Change user username",
    description="Set user username in the database"
)
async def modify_username(
    data: ChangeUsernameSchema,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
):
    
    new_access_token = None
    access_token = credentials.credentials

    # Access token check
    user_id = get_user_id_from_access_token(access_token)
    
    # If access token is expired, refresh
    if user_id is None:
        # Refresh access token and get user id
        new_access_token = refresh_access_token(refresh_token, db)  # get new access token
        access_token = new_access_token.access_token                # update access token
        refresh_token = new_access_token.refresh_token              # update refresh token
        user_id = get_user_id_from_access_token(access_token)       # get user id

    user = await change_user_username(user_id, data.new_username, db)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.active,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }


# Change email
@router.put(
        "/email/", 
        response_model=UserSchema,
        summary="Change user email",
        description="Set user email in the database"
    )
async def modify_email(
    data: ChangeEmailSchema,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
):

    new_access_token = None
    access_token = credentials.credentials

    # Access token check
    user_id = get_user_id_from_access_token(access_token)
    
    # If access token is expired, refresh
    if user_id is None:
        # Refresh access token and get user id
        new_access_token = refresh_access_token(refresh_token, db)  # get new access token
        access_token = new_access_token.access_token                # update access token
        refresh_token = new_access_token.refresh_token              # update refresh token
        user_id = get_user_id_from_access_token(access_token)       # get user id

    user = await change_user_email(user_id, data.new_email, db)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.active,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }


# Change password
@router.put(
        "/password/", 
        response_model=UserSchema,
        summary="Change user password",
        description="Set user password in the database"
    )
async def modify_password(
    data: ChangePasswordSchema,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
):

    new_access_token = None
    access_token = credentials.credentials

    # Access token check
    user_id = get_user_id_from_access_token(access_token)
    
    # If access token is expired, refresh
    if user_id is None:
        # Refresh access token and get user id
        new_access_token = refresh_access_token(refresh_token, db)  # get new access token
        access_token = new_access_token.access_token                # update access token
        refresh_token = new_access_token.refresh_token              # update refresh token
        user_id = get_user_id_from_access_token(access_token)       # get user id

    user = await change_user_password(
        user_id=user_id, 
        old_password=data.old_password, 
        new_password=data.new_password, 
        db=db
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.active,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }