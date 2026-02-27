# =========================
# Roles management service
# =========================

# Imports
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends
from typing import Annotated
# Services
from ..services.role_management.add_role_for_user import add_role_for_users
from ..services.role_management.remove_role_from_user import remove_role_from_users
# Dependencies
from ..dependencies.data_base_connection import get_db
from ..dependencies.admin_dependency import get_admin_user_id
# Schemas
from ..schemas.roles.role_assignment_schema import RoleAssignmentSchema
from ..schemas.roles.role_operation_response_schema import RoleOperationResponseSchema


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
@router.post("/add", response_model=RoleOperationResponseSchema)
async def add_role_for_user_endpoint(
    data: RoleAssignmentSchema,
    db: Annotated[AsyncSession, Depends(get_db)],    # DB session
    admin_user_id: int = Depends(get_admin_user_id),
):
    """
    Add a role to multiple users.

    Steps:
    1. Extract access token from header
    2. Verify that requester is admin
    3. Call service to add role for users
    4. Return result
    """

    return await add_role_for_users(
        user_ids=data.user_ids, 
        role_id=data.role_id, 
        db=db, 
        user_id=admin_user_id
    )


# =========================
# Remove role from users endpoint
# =========================
@router.post("/remove", response_model=RoleOperationResponseSchema)
async def remove_role_from_user_endpoint(
    data: RoleAssignmentSchema,
    db: Annotated[AsyncSession, Depends(get_db)],    # DB session
    admin_user_id: int = Depends(get_admin_user_id),
):
    """
    Remove a role from multiple users.

    Steps:
    1. Extract access token from header
    2. Verify that requester is admin
    3. Call service to remove role from users
    4. Return result
    """
    
    return await remove_role_from_users(
        user_ids=data.user_ids, 
        role_id=data.role_id, 
        db=db, 
        user_id=admin_user_id
    )