# =========================
# Authentication service
# =========================

# Imports
# Libraries
from fastapi import (
    APIRouter, 
    Depends, 
    Request
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordRequestForm
)
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
import os
from urllib.parse import urlencode
# Schemas
from ..schemas.auth.registration_schema import RegistrationSchema
from ..schemas.auth.login_schema import LoginSchema
from ..schemas.tokens.token_refresh_schema import TokenRefreshSchema
# Services
from ..services.auth.registration_service import register_user
from ..services.auth.login_service import login_user
from ..services.auth.logout_service import logout
from ..services.auth.google_auth_service import google_auth_callback
# Dependencies
from ..dependencies.data_base_connection import get_db


# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/auth",
    tags=["Auth service"]
)


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenRefreshSchema,
    summary="Authenticate a user",
)
async def user_login_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    '''
    Login user:

    1. Extract username and password
    2. Create LoginSchema instance
    3. Call login_user service
    '''
    data = LoginSchema(
        username=form_data.username,
        password=form_data.password
    )

    return await login_user(db=db, data=data)


# ============================================================
# GOOGLE OAUTH SETUP 
#
# use this for test:
# http://localhost:8000/auth/google/login - login
# http://localhost:8000/auth/google/callback - callback redirect to frontend
# ============================================================

oauth = OAuth()

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile",
    },
)


# ============================================================
# GOOGLE LOGIN REDIRECT
# ============================================================

@router.get("/google/login")
async def get_google_login(request: Request):
    '''
    Redirect to Google login
    use this for test:
    http://localhost:8000/auth/google/login
    '''
    redirect_uri = request.url_for("google_auth_handler")
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


# ============================================================
# GOOGLE CALLBACK
# ============================================================

@router.get("/google/callback")
async def google_auth_handler(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    '''
    Handle Google callback
    '''
    tokens = await google_auth_callback(oauth, db, request)

    frontend_url = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173/login"
    )

    query = urlencode({
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    })

    return RedirectResponse(
        url=f"{frontend_url}?{query}",
        status_code=303
    )


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    summary="Create a new user",
    response_model=TokenRefreshSchema
)
async def user_registration_endpoint(
    data: RegistrationSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    '''
    Register user:

    1. Extract username, email and password
    2. Create RegistrationSchema instance
    3. Call register_user service
    '''
    return await register_user(data=data, db=db)


# ============================================================
# LOGOUT
# ============================================================

logout_scheme = HTTPBearer()


@router.post(
    "/logout",
    summary="Logout a user"
)
async def logout_user_endpoint(
    data: Annotated[
        HTTPAuthorizationCredentials,
        Depends(logout_scheme)
    ],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    '''
    Logout user:

    1. Extract refresh token
    2. Call logout service
    '''
    refresh_token = data.credentials
    return await logout(db=db, refresh_token=refresh_token)