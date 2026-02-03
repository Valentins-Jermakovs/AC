# Imports
from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from ..schemas.pagination_schema import PaginatedUsers
from ..schemas.user_schema import UserSchema
from ..services.user_read_service import (
    get_users_paginated,
    get_user_by_id, 
    get_user_by_username_or_email, 
    get_users_by_role
)
from ..services.admin_required_service import admin_required
from ..services.refresh_tokens_service import (
    refresh_access_token, 
    get_user_id_from_access_token
)
from ..dependencies.data_base_connection import get_db


# Router
router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

security = HTTPBearer()

# All users
@router.get(    # router path
    "/",
    response_model=PaginatedUsers,
    summary="Get all users paginated",
    description="Get all users from the database",
)
async def fetch_all_users_paginated(    # business logic
    db: Annotated[Session, Depends(get_db)],   
    page: int = 1,
    limit: int = 10,
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

    # Check admin role
    admin_required(user_id, db)

    paginated_users = await get_users_paginated(db, page, limit)

    return {
        "items": paginated_users.items,
        "meta": paginated_users.meta,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }

# User by ID
@router.get(    # router path
    "/{find_user_id}", 
    response_model=PaginatedUsers,
    summary="Get user by ID",
    description="Get user by ID from the database"
)
async def fetch_user_by_id(  # business logic
    find_user_id: int, 
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

    # Check admin role
    admin_required(user_id, db)

    user = await get_user_by_id(find_user_id, db)

    return {
        "items": [user],
        "meta": None,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }

# User by username or email
@router.get(    # router path
    "/search/{name_or_email}", 
    response_model=PaginatedUsers,
    summary="Get user by username or email",
    description="Get user by username or email from the database"
)
async def fetch_user_by_username_or_email(  # business logic
    name_or_email: str,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    limit: int = 10,
):
    return get_user_by_username_or_email(name_or_email, db, page, limit)

# Users by role
@router.get(    # router path
    "/role/{role}", 
    response_model=PaginatedUsers,
    summary="Get users by role",
    description="Get users by role from the database"
)
async def fetch_users_by_role(  # business logic
    role: str,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    limit: int = 10,
):
    return get_users_by_role(role, db, page, limit)