# Imports
from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session

from ..schemas.users.pagination_schema import PaginatedUsers

from ..services.read_users.read_all_users_service import get_users_paginated
from ..services.read_users.read_user_by_id_service import get_user_by_id
from ..services.read_users.read_user_by_name_or_email_service import get_user_by_username_or_email
from ..services.read_users.read_user_by_role_service import get_users_by_role

from ..dependencies.data_base_connection import get_db

# Router
router = APIRouter(
    prefix="/users", 
    tags=["Users read service"]
)

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
):
    paginated_users = await get_users_paginated(db, page, limit)

    return {
        "items": paginated_users.items,
        "meta": paginated_users.meta,
    }

# User by ID
@router.get(    # router path
    "/{find_user_by_id}", 
    response_model=PaginatedUsers,
    summary="Get user by ID",
    description="Get user by ID from the database"
)
async def fetch_user_by_id(  # business logic
    find_user_by_id: int, 
    db: Annotated[Session, Depends(get_db)],
):

    user = await get_user_by_id(find_user_by_id, db)

    return {
        "items": [user],
        "meta": None,
    }


# User by username or email
@router.get(    # router path
    "/search/{name_or_email}",
    response_model=PaginatedUsers,
    summary="Get user by username or email",
    description="Get user by username or email from the database",
)
async def fetch_user_by_username_or_email(  # business logic
    name_or_email: str,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    limit: int = 10,
    # Access token from Authorization: Bearer <token>
):

    users = await get_user_by_username_or_email(name_or_email, db, page, limit)

    return {
        "items": users.items,
        "meta": users.meta,
    }

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

    users = await get_users_by_role(role, db, page, limit)

    return {
        "items": users.items,
        "meta": users.meta,
    }