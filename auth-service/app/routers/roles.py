# ===== Importi =====
from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_schema import UserSchema

from ..services.base_connection import engine
from ..services.user_role_service import change_role_for_users

from ..dependencies.data_base_connection import get_db

# ===== Ceļa definēšana (/roles) =====
router = APIRouter(prefix="/roles", tags=["Roles"])


@router.put("/", response_model=list[UserSchema],
             summary="Change users roles",
             description="Set user role in the database"
             )
async def change_user_role(
    user_ids: list[int],
    role_name: str,
    db: Annotated[Session, Depends(get_db)]
):
    return change_role_for_users(user_ids, role_name, db)