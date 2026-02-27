# =========================
# Users read service
# =========================

# Imports
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
# Schemas
from ..schemas.users.pagination_schema import PaginatedUsersSchema
from ..schemas.users.user_schema import UserSchema
# Services
from ..services.read_users.read_all_users_service import get_users_paginated
from ..services.read_users.read_user_by_id_service import get_user_by_id
from ..services.read_users.read_user_by_name_or_email_service import get_user_by_username_or_email
from ..services.read_users.read_user_by_role_service import get_users_by_role
# Dependencies
from ..dependencies.data_base_connection import get_db
from ..dependencies.admin_dependency import get_admin_user_id
# Utils
from ..utils.check_access_token import check_access_token


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/users",    # All endpoints start with /users
    tags=["Users read service [Mostly for admins]"] # Tag for documentation
)

# Security scheme for access token
security = HTTPBearer()

# =========================
# Get all users (paginated)
# =========================
@router.get(
    "/",
    response_model=PaginatedUsersSchema,
    summary="Get all users paginated",
)
async def fetch_all_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user_id: int = Depends(get_admin_user_id),
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

    paginated_users = await get_users_paginated(
        db=db, 
        page=page, 
        limit=limit
    )

    return paginated_users

# =========================
# Get info about current user
# =========================
@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get info about current user",
)
async def fetch_current_user_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
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
    "/{user_id}", 
    response_model=UserSchema,
    summary="Get user by ID",
)
async def fetch_user_by_id_endpoint(
    find_user_by_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user_id: int = Depends(get_admin_user_id),
):
    """
    Retrieve one user by ID.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Fetch user by ID from DB
    4. Return as single-item list
    """

    user = await get_user_by_id(
        user_id=find_user_by_id, 
        db=db
    )

    return user


# =========================
# Get user by username or email
# =========================
@router.get(
    "/search/{name_or_email}",
    response_model=PaginatedUsersSchema,
    summary="Get user by username or email",
)
async def fetch_user_by_username_or_email_endpoint(
    name_or_email: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user_id: int = Depends(get_admin_user_id),
    page: int = 1,
    limit: int = 10,
):
    """
    Search for users by username or email.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Search users in DB with pagination
    4. Return items and metadata
    """

    users = await get_user_by_username_or_email(
        username_or_email=name_or_email, 
        db=db, 
        page=page, 
        limit=limit
    )

    return users


# =========================
# Get users by role
# =========================
@router.get(    # router path
    "/role/{role}", 
    response_model=PaginatedUsersSchema,
    summary="Get users by role",
)
async def fetch_users_by_role_endpoint(  # business logic
    role: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user_id: int = Depends(get_admin_user_id),
    page: int = 1,
    limit: int = 10,
):
    '''
    Get users by role.

    Steps:
    1. Extract access token
    2. Verify admin role
    3. Get users by role from DB
    4. Return items and metadata
    '''

    users = await get_users_by_role(
        role=role, 
        db=db, 
        page=page, 
        limit=limit
    )

    return users