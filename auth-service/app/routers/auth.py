# ===== Importi =====
from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from sqlmodel import Session

from ..schemas.registration_schema import RegistrationSchema
from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from ..schemas.refresh_schema import RefreshSchema

from ..services.registration_service import register_user
from ..services.auth_service import login_user

from ..services.refresh_service import (
    get_user_id_from_access_token,
    refresh_access_token
)

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

# ===== Access token pārbaude =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/check",
             summary="Check access token",
             description="Check access token"
             )
async def check(
        access_token: str = Depends(oauth2_scheme),
    ):
    user_id = get_user_id_from_access_token(access_token)
    return {
        "user_id": user_id, 
        "message": "Access token is valid"
    }

# ===== Refresh token pārbaude =====
# prasa header Authorization: Bearer <token>
refresh_scheme = HTTPBearer(auto_error=True)
@router.post("/refresh", response_model=TokenWithRefreshSchema,
             summary="Refresh access token",
             description="Refresh access token"
             )
async def refresh(
        data: Annotated[
            HTTPAuthorizationCredentials, Depends(refresh_scheme)
        ],
        db: Annotated[Session, Depends(get_db)]
    ):
    refresh_token = data.credentials # string no header
    return refresh_access_token(db, refresh_token)
