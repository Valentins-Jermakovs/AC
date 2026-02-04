# Imports
from fastapi import APIRouter, Depends, Header, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

@router.put(
    "/",
    response_model=ChangeRoleResponseSchema,
)
async def change_user_role(
    user_ids: list[int],
    role_name: str,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
):
    access_token = credentials.credentials
    new_tokens = None
    user_id = get_user_id_from_access_token(access_token)

    # Ja token beidzies → atjauno
    if user_id is None:
        new_tokens = refresh_access_token(refresh_token, db)
        user_id = get_user_id_from_access_token(new_tokens.access_token)

    try:
        # Admin pārbaude
        admin_required(user_id, db)
        # Lomu maiņa
        users = change_role_for_users(user_ids, role_name, db)
        return {"users": users}

    finally:
        # Tokeni vienmēr tiek ielikti headeros, pat ja kļūda notiek
        if new_tokens:
            response.headers["X-Access-Token"] = new_tokens.access_token
            response.headers["X-Refresh-Token"] = new_tokens.refresh_token
