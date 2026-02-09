# =========================
# Authentication service
# =========================

# Imports
from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import (
    HTTPBearer, 
    HTTPAuthorizationCredentials, 
    OAuth2PasswordRequestForm
)
from authlib.integrations.starlette_client import OAuth
import os
from typing import Annotated
from sqlmodel import Session
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
    prefix="/auth", # All auth endpoints start with /auth
    tags=["Auth service"]   # Tag for docs grouping
)


# =========================
# User login endpoint
# =========================
@router.post(
    "/login",
    response_model=TokenRefreshSchema,
    summary="Authenticate a user",
    description="OAuth2 compatible login"
)
async def user_authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], # Form data: username + password
    db: Annotated[Session, Depends(get_db)] # DB session
):
    """
    Authenticates a user using username and password.

    Steps:
    1. Get username and password from form
    2. Call login_user service to validate and generate tokens
    3. Return access and refresh tokens
    """
    data = LoginSchema( # get form data
        username=form_data.username,
        password=form_data.password
    )
    return await login_user(db, data)


# =========================
# Google OAuth setup
# =========================
oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile",    # Request email and profile info
    },
)


# http://localhost:8000/auth/google/login
# =========================
# Google login endpoint
# =========================
@router.get("/google/login", response_model=None)
async def get_google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# =========================
# Google callback endpoint
# =========================
@router.get("/google/callback", response_model=TokenRefreshSchema)
async def google_auth_handler(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Handles Google OAuth callback and generates tokens.

    Steps:
    1. Receive callback from Google
    2. Authenticate user or create new one
    3. Generate access and refresh tokens
    """
    return await google_auth_callback(oauth, db, request)

# =========================
# User registration endpoint
# =========================
@router.post(
    "/register",
    summary="Create a new user", 
    description="Get JSON data and create a new user in the database",
    response_model=TokenRefreshSchema
)
async def user_registration(
    data: Annotated[RegistrationSchema,
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
    """
    Register a new user and return access/refresh tokens.

    Steps:
    1. Get user data from JSON body
    2. Call register_user service
    3. Return generated tokens
    """
    register_user_with_token = await register_user(data, db)
    return register_user_with_token


# =========================
# User logout endpoint
# =========================
logout_scheme = HTTPBearer()    # Extract refresh token from header
@router.post(
    "/logout",
    summary="Logout a user", 
    description="Get JSON data and logout a user in the database"
)
async def logout_user(
    data: Annotated[HTTPAuthorizationCredentials, Depends(logout_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Logout user by deleting refresh token.

    Steps:
    1. Get refresh token from HTTP header
    2. Call logout service to remove it from DB
    3. Return confirmation message
    """
    refresh_token = data.credentials
    return await logout(db, refresh_token)
