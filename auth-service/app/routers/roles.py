from ..services.role_management.add_role_for_user import add_role_for_users
from ..services.role_management.remove_role_from_user import remove_role_from_users
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ..dependencies.data_base_connection import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.check_admin_role import check_admin_role
from typing import Annotated

# Router
router = APIRouter(
    prefix="/roles", 
    tags=["Roles management service"], 
)

# Add role for users
@router.post("/add")
async def add_role_for_user(
    user_ids: list[int], 
    role_id: int, 
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    access_token = credentials.credentials
    # Check admin role
    user_id = await check_admin_role(access_token, db)
    return await add_role_for_users(user_ids, role_id, db)

# Remove role from users
@router.post("/remove")
async def remove_role_from_user(
    user_ids: list[int], 
    role_id: int, 
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    access_token = credentials.credentials
    # Check admin role
    user_id = await check_admin_role(access_token, db)
    return await remove_role_from_users(user_ids, role_id, db)