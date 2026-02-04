# Imports
from fastapi import (
    APIRouter, 
    Depends,
    Header
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from ..schemas.user_active_schema import UserActiveSchema
from ..services.user_activity_service import change_users_activity_status
from ..dependencies.data_base_connection import get_db
from ..services.admin_required_service import admin_required
from ..services.refresh_tokens_service import (
    refresh_access_token, 
    get_user_id_from_access_token
)

# Router
router = APIRouter(
    prefix="/activity", 
    tags=["Activity"]
)

security = HTTPBearer()

# Change users activity status
@router.put(
    "/",
    summary="Change users activity status",
    description="Set user activity status in the database"
)
async def change_user_activity_status(
    user_ids: list[int],
    is_active: bool,
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

    users = await change_users_activity_status(user_ids, is_active, db)

    return {
        "users": users,
        "access_token": new_access_token.access_token if new_access_token else None,
        "refresh_token": new_access_token.refresh_token if new_access_token else None
    }