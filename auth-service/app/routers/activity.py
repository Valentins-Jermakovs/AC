# Šis fails atbilst par lietotāju aktivitātes statusa maiņu

from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_active_schema import UserActiveSchema
from ..services.base_connection import engine
from ..services.user_activity_service import change_users_activity_status

# === definē ceļu /activity ===
router = APIRouter(prefix="/activity", tags=["Activity"])

# === veidojam savienojumu ar DB ===
def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()


# === lietotāju aktivitātes statusa maiņas funkcija ===
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