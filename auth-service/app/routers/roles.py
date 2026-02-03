# Imports
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Header, HTTPException, status

from sqlmodel import Session
from typing import Annotated
from ..schemas.change_role_response_schema import ChangeRoleResponseSchema
from ..services.user_role_service import change_role_for_users
from ..services.admin_required_service import admin_required
from ..services.refresh_tokens_service import (
    refresh_access_token, 
    get_user_id_from_access_token
)
from ..dependencies.data_base_connection import get_db

"""
===== Roles management API =====
This router contains endpoints related to user role management.
All routes under this router require proper authentication and authorization.
Role changes are restricted to users with administrator privileges.

Change roles for multiple users.

Flow:
- Validate access token and extract user ID
- Refresh access token if it has expired
- Verify that the current user has administrator privileges
- Update roles for the specified users
- Return updated users and refreshed tokens if applicable

Returns:
- List of updated users
- New access and refresh tokens if the access token was refreshed
"""

# Router
router = APIRouter(
    prefix="/roles", 
    tags=["Roles"], 
)

security = HTTPBearer()

@router.put( # router path
    "/", 
    response_model=ChangeRoleResponseSchema,
    summary="Change users roles",
    description="Set user role in the database",
)
async def change_user_role( # business logic
    user_ids: list[int],
    role_name: str,
    db: Annotated[Session, Depends(get_db)],
    # Access token no Authorization: Bearer <token>
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

    # Change user role
    users = change_role_for_users(user_ids, role_name, db)

    return {
        "users": users,
        # If access token is expired, refresh and return it to the client
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }