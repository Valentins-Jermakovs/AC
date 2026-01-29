# Šis fails atbild par lomu maiņu lietotājiem

from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_schema import UserSchema
from ..services.base_connection import engine
from ..services.user_role_service import change_role_for_users

# === definē ceļu /roles ===
router = APIRouter(prefix="/roles", tags=["Roles"])

# === veidojam savienojumu ar DB ===
def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()

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