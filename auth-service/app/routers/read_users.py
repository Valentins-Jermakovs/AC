# =========================
# Users read service
# =========================

# Imports
from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
# Schemas
from ..schemas.users.pagination_schema import PaginatedUsers
from ..schemas.users.user_schema import UserSchema
# Services
from ..services.read_users.read_all_users_service import get_users_paginated
from ..services.read_users.read_user_by_id_service import get_user_by_id
from ..services.read_users.read_user_by_name_or_email_service import get_user_by_username_or_email
from ..services.read_users.read_user_by_role_service import get_users_by_role
# Dependencies
from ..dependencies.data_base_connection import get_db
# Utils
from ..utils.check_admin_role import check_admin_role
from ..utils.check_access_token import check_access_token


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/users",    # All endpoints start with /users
    tags=["Users read service"] # Tag for documentation
)

# Security scheme for access token
security = HTTPBearer()

# =========================
# Get all users (paginated)
# =========================
@router.get(
    "/",
    response_model=PaginatedUsers,
    summary="Get all users paginated",
    description="Get all users from the database",
)
async def fetch_all_users_paginated(
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
    page: int = 1,
    limit: int = 10,
):
    """
    Retrieve all users with pagination.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Get paginated users from DB
    4. Return items and metadata
    """
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)

    paginated_users = await get_users_paginated(db, page, limit)

    return {
        "items": paginated_users.items,
        "meta": paginated_users.meta,
    }

# =========================
# Get info about current user
# =========================
@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get info about current user",
    description="Get info about current user from the database",
)
async def fetch_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Retrieve info about current user.

    Steps:
    1. Extract access token
    2. Extract user ID
    3. Fetch user info from DB
    4. Return as single-item list
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    user = await get_user_by_id(user_id, db)

    return user



# =========================
# Get user by ID
# =========================
@router.get(
    "/{find_user_by_id}", 
    response_model=UserSchema,
    summary="Get user by ID",
    description="Get user by ID from the database"
)
async def fetch_user_by_id(
    find_user_by_id: int, 
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Retrieve one user by ID.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Fetch user by ID from DB
    4. Return as single-item list
    """
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)

    user = await get_user_by_id(find_user_by_id, db)

    return user


# =========================
# Get user by username or email
# =========================
@router.get(
    "/search/{name_or_email}",
    response_model=PaginatedUsers,
    summary="Get user by username or email",
    description="Get user by username or email from the database",
)
async def fetch_user_by_username_or_email(
    name_or_email: str,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
):
    """
    Search for users by username or email.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Search users in DB with pagination
    4. Return items and metadata
    """
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)

    users = await get_user_by_username_or_email(name_or_email, db, page, limit)

    return {
        "items": users.items,
        "meta": users.meta,
    }


# =========================
# Get users by role
# =========================
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
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Access token from header
):
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)

    users = await get_users_by_role(role, db, page, limit)

    return {
        "items": users.items,
        "meta": users.meta,
    }