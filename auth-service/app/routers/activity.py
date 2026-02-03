# ===== Importi =====
from fastapi import (
    APIRouter, 
    Depends
)
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_active_schema import UserActiveSchema

from ..services.user_activity_service import change_users_activity_status

from ..dependencies.data_base_connection import get_db
from ..dependencies.admin_required import admin_required

# ===== Ceļa definēšana (/activity) =====
router = APIRouter(prefix="/activity", tags=["Activity"], dependencies=[Depends(admin_required)])


# ===== Visu lietotāju aktivitātes statusa maiņa =====
@router.put("/", response_model=list[UserActiveSchema],
             summary="Change users activity status",
             description="Set user activity status in the database"
             )
async def change_user_activity_status(
    user_ids: list[int],
    is_active: bool,
    db: Annotated[Session, Depends(get_db)]
):
    return change_users_activity_status(user_ids, is_active, db)