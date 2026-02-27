# =========================
# Users activity management service
# =========================

# Imports
from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
# Services
from ..services.activity_management.change_users_activity_service import change_users_activity_status
# Dependencies
from ..dependencies.data_base_connection import get_db
# Utils
from ..utils.check_admin_role import check_admin_role
# Schemas
from ..schemas.users.user_activity_schema import UserActivitySchemaData, UserActivitySchemaResponse


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/activity", # All endpoints in this router start with /activity
    tags=["Users activity management service [Only for admins]"]  # Tag for documentation grouping
)


# =========================
# Change users activity status
# =========================
@router.put(
    "/",
    summary="Change users activity status", # Short description for docs
    response_model=list[UserActivitySchemaResponse]
)
async def change_user_activity_status_endpoint(
    data: UserActivitySchemaData,
    db: Annotated[AsyncSession, Depends(get_db)],    # DB session injected automatically
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    # Require HTTP Bearer token for authentication
):
    """
    Updates the activity status of users.

    Steps:
    1. Extract access token from credentials
    2. Verify that user is admin
    3. Update activity status for given user IDs
    4. Return updated users
    """

    # Extract token from HTTP credentials
    access_token = credentials.credentials

    # Verify admin role, raise error if user is not admin
    user_id = await check_admin_role(access_token, db)

    # Update activity status for users in DB
    users = await change_users_activity_status(
        user_ids=data.user_ids, 
        is_active=data.is_active, 
        db=db, 
        user_id=user_id
    )

    # Return updated user info
    return users