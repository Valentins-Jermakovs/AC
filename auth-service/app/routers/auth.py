# ===== Importi =====
from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session
from sqlmodel import Session

from ..schemas.registration_schema import RegistrationSchema
from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema

from ..services.registration_service import register_user
from ..services.auth_service import login_user

from ..dependencies.data_base_connection import get_db

# ===== Ceļa definēšana (/auth) =====
router = APIRouter(prefix="/auth", tags=["Auth"])

# ===== Reģistrācijas mehānisms =====
@router.post("/register", 
             summary="Create a new user", 
             description="Get JSON data and create a new user in the database",
             response_model=TokenWithRefreshSchema
             )
async def register(
        data: Annotated[
        RegistrationSchema,
        Body(
            example={
                "username": "testuser", 
                "email": "test@inbox.lv", 
                "password": "12345678"
            }
        )
    ],
    db: Annotated[Session, Depends(get_db)]
):

    register_user_with_token = register_user(data, db)

    return register_user_with_token


# ===== Logošanas mehānisms =====
@router.post("/login", 
             summary="Login a user", 
             description="Get JSON data and login a user in the database",
             response_model=TokenWithRefreshSchema
             )
async def login(
        data: Annotated[
        LoginSchema,
        Body(
            example={
                "username": "testuser", 
                "password": "12345678"
            }
        )
    ],
    db: Annotated[Session, Depends(get_db)]
):

    return login_user(db, data)

