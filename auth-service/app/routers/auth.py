from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.registration_schema import RegistrationSchema
from ..schemas.auth_schema import LoginSchema
from ..schemas.user_schema import UserSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from ..services.user_service import register_user
from ..services.login_service import login_user
from ..services.base_connection import engine
from sqlmodel import Session

# === definē ceļu /auth ===
router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()

# === reģistrācijas mehānisms ===
@router.post("/register", 
             summary="Create a new user", 
             description="Get JSON data and create a new user in the database",
             response_model=TokenWithRefreshSchema
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
    register_user_with_token = register_user(data, db)
    # atgriež klientam informāciju (tokeni)
    return register_user_with_token
# === === === === === === === === === === === === === === ===

# === login mehānisms ===
@router.post("/login", 
             summary="Login a user", 
             description="Get JSON data and login a user in the database",
             response_model=TokenWithRefreshSchema
             )
async def login(
        data: Annotated[
        LoginSchema,
        Body(
            example={"username": "testuser", "password": "12345678"}
        )
    ],
    db: Annotated[Session, Depends(get_db)]
):
    # atgriež klientam informāciju (tokeni)
    return login_user(db, data)
# === === === === === === === === === === === === === === ===
