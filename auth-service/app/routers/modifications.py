# Šis fails atbilst par lietotāju modificēšanas operācijām
#   - lietotāju vārda maiņa
#   - lietotāju epastu maiņa
#   - lietotāju paroli maiņa

from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_schema import UserSchema
from ..services.base_connection import engine
from ..services.user_modification_service import change_user_username, change_user_email, change_user_password

# === definē ceļu /modifications ===
router = APIRouter(prefix="/modifications", tags=["Modifications"])

# === veidojam savienojumu ar DB ===
def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()


# === lietotāju vārda maiņa ===
@router.put("/username/{user_id}", response_model=UserSchema)
async def modify_username(user_id: int, new_username: str, db: Annotated[Session, Depends(get_db)]):
    return change_user_username(user_id, new_username, db)

# === lietotāju epastu maiņa ===
@router.put("/email/{user_id}", response_model=UserSchema)
async def modify_email(user_id: int, new_email: str, db: Annotated[Session, Depends(get_db)]):
    return change_user_email(user_id, new_email, db)

# === lietotāju paroli maiņa ===
@router.put("/password/{user_id}", response_model=UserSchema)
async def modify_password(user_id: int, old_password: str, new_password: str, db: Annotated[Session, Depends(get_db)]):
    return change_user_password(user_id, old_password, new_password, db)