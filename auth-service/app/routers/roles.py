from ..services.role_management.add_role_for_user import add_role_for_users
from ..services.role_management.remove_role_from_user import remove_role_from_users
from ..services.role_management.get_user_roles import get_user_roles
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ..dependencies.data_base_connection import get_db

# Router
router = APIRouter(
    prefix="/roles", 
    tags=["Roles management service"], 
)

# Get user roles
@router.get("/{user_id}")
async def read_user_roles(user_id: int, db: Session = Depends(get_db)):
    return await get_user_roles(user_id, db)

# Add role for users
@router.post("/add")
async def add_role_for_user(user_ids: list[int], role_id: int, db: Session = Depends(get_db)):
    return await add_role_for_users(user_ids, role_id, db)

# Remove role from users
@router.post("/remove")
async def remove_role_from_user(user_ids: list[int], role_id: int, db: Session = Depends(get_db)):
    return await remove_role_from_users(user_ids, role_id, db)