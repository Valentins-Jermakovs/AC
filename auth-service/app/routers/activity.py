# Imports
from fastapi import (
    APIRouter, 
    Depends,
    Header,
    Response
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from ..schemas.users.user_activity_schema import UserActivitySchema

from ..services.activity_management.change_users_activity_service import change_users_activity_status
from ..dependencies.data_base_connection import get_db
from ..utils.check_admin_role import check_admin_role

# Router
router = APIRouter(
    prefix="/activity", 
    tags=["Users activity management service"]
)

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
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    access_token = credentials.credentials
    # Check admin role
    user_id = await check_admin_role(access_token, db)
    users = await change_users_activity_status(user_ids, is_active, db)

    return users