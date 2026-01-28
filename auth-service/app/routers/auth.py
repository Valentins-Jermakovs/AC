from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.registration_schema import RegistrationSchema
from ..services.user_service import register_user
from ..services.base_connection import engine
from sqlmodel import Session

# definē ceļu /auth
router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()

# reģistrācijas mehānisms
@router.post("/register", 
             summary="Create a new user", 
             description="Get JSON data and create a new user in the database"
             )
async def register(
        data: Annotated[
        RegistrationSchema,
        Body(
            example={"username": "testuser", "email": "test@inbox.lv", "password": "12345678"}
        )
    ],
    db: Annotated[Session, Depends(get_db)]
):
    # saņem lietotāju
    user =  await register_user(data, db)
    # atgriež klientam informāciju (tests - pēc tam aizvietot uz tokenu)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
