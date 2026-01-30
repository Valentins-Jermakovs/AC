# ===== Importi =====
from fastapi import (
    APIRouter, 
    Depends,
    Query
)
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_schema import UserSchema

from ..services.user_modification_service import (
    change_user_username, 
    change_user_email, 
    change_user_password
)

from ..dependencies.data_base_connection import get_db

# ===== Ceļa definēšana (/modifications) =====
router = APIRouter(prefix="/modifications", tags=["Modifications"])


# ===== Lietotāja vārda maiņa =====
@router.put(
        "/username/{user_id}", 
        response_model=UserSchema
        )
async def modify_username(
        user_id: int, 
        new_username: str, 
        db: Annotated[Session, Depends(get_db)]
    ):
    return change_user_username(
        user_id, 
        new_username, 
        db
    )

# ===== Lietotāja epasta maiņa =====
@router.put(
        "/email/{user_id}", 
        response_model=UserSchema
    )
async def modify_email(
        user_id: int, 
        new_email: str, 
        db: Annotated[Session, Depends(get_db)]
    ):
    return change_user_email(
        user_id, 
        new_email, 
        db
    )

# ===== Lietotāja paroles maiņa =====
@router.put(
        "/password/{user_id}", 
        response_model=UserSchema
    )
async def modify_password(
        user_id: int,
        new_password: str, 
        db: Annotated[Session, Depends(get_db)],
        old_password: str | None = Query(default=None)
    ):
    return change_user_password(
        user_id, 
        old_password, 
        new_password, 
        db
    )