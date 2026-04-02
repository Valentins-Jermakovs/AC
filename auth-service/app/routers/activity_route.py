# =========================
# Users activity management service
# =========================

# Imports
from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Services
from ..services.activity_management.change_users_activity_service import change_users_activity_status, change_user_activity_status
# Dependencies
from ..dependencies.data_base_connection import get_db
from ..dependencies.admin_dependency import get_admin_user_id
# Schemas
from ..schemas.users.user_activity_schema import UserActivitySchemaData, UserActivitySchemaResponse, OneUserActivitySchemaData
# Utils
from app.utils.check_access_token import check_access_token


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/activity", # All endpoints in this router start with /activity
    tags=["Users activity management service [Only for admins]"]  # Tag for documentation grouping
)

# Security scheme for access token
security = HTTPBearer()


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
    admin_user_id: int = Depends(get_admin_user_id),
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

    # Update activity status for users in DB
    users = await change_users_activity_status(
        user_ids=data.user_ids, 
        is_active=data.is_active, 
        db=db, 
        user_id=admin_user_id
    )

    # Return updated user info
    return users

# =========================
# Change user activity status
# =========================
@router.put(
    "/me",
    summary="Change user activity status", # Short description for docs
    response_model=UserActivitySchemaResponse
)
async def change_user_activity_status_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],    # DB session injected automatically
    credantials: HTTPAuthorizationCredentials = Depends(security)
    # Require HTTP Bearer token for authentication
):
    """
    Updates the activity status of a single user.

    Steps:
    1. Extract access token from credentials
    2. Verify that user is admin
    3. Update activity status for given user ID
    4. Return updated user
    """

    # Extract access token
    access_token = credantials.credentials

    # Verify access token
    user_id = await check_access_token(access_token)

    # Update activity status for user in DB
    user = await change_user_activity_status(
        user_id=user_id, 
        db=db,
    )

    # Return updated user info
    return user