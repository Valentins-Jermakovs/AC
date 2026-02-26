# =========================
# Roles management service
# =========================

# Imports
from sqlmodel import Session
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
# Services
from ..services.role_management.add_role_for_user import add_role_for_users
from ..services.role_management.remove_role_from_user import remove_role_from_users
# Dependencies
from ..dependencies.data_base_connection import get_db
# Utils
from ..utils.check_admin_role import check_admin_role


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/roles",    # All endpoints start with /roles
    tags=["Roles management service"],  # Tag for docs grouping
)


# =========================
# Add role for users endpoint
# =========================
@router.post("/add")
async def add_role_for_user(
    user_ids: list[int],    # List of user IDs to add role
    role_id: int,           # Role ID to add
    db: Annotated[Session, Depends(get_db)],    # DB session
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] # Access token
):
    """
    Add a role to multiple users.

    Steps:
    1. Extract access token from header
    2. Verify that requester is admin
    3. Call service to add role for users
    4. Return result
    """
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)

    return await add_role_for_users(
        user_ids=user_ids, 
        role_id=role_id, 
        db=db, 
        user_id=user_id
    )


# =========================
# Remove role from users endpoint
# =========================
@router.post("/remove")
async def remove_role_from_user(
    user_ids: list[int],    # List of user IDs to remove role
    role_id: int,           # Role ID to remove
    db: Annotated[Session, Depends(get_db)],    # DB session
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] # Access token
):
    """
    Remove a role from multiple users.

    Steps:
    1. Extract access token from header
    2. Verify that requester is admin
    3. Call service to remove role from users
    4. Return result
    """
    access_token = credentials.credentials
    user_id = await check_admin_role(access_token, db)
    
    return await remove_role_from_users(
        user_ids=user_ids, 
        role_id=role_id, 
        db=db, 
        user_id=user_id
    )