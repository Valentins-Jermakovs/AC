# Imports
from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import (
    HTTPBearer, 
    HTTPAuthorizationCredentials, 
    OAuth2PasswordRequestForm
)
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session
from dotenv import load_dotenv
import os
from typing import Annotated
from sqlmodel import Session
from ..schemas.auth.registration_schema import RegistrationSchema
from ..schemas.auth.login_schema import LoginSchema
from ..schemas.tokens.token_refresh_schema import TokenRefreshSchema
from ..services.auth.registration_service import register_user
from ..services.auth.login_service import login_user
from ..services.auth.logout_service import logout
from ..services.auth.google_auth_service import get_google_auth, google_auth_callback
from ..dependencies.data_base_connection import get_db


"""
Auth Router

This module defines the authentication-related endpoints for the application under the "/auth" prefix.

Endpoints:

1. POST /auth/login
   - Purpose: Authenticate a user with username and password.
   - Input: OAuth2PasswordRequestForm containing 'username' and 'password'.
   - Output: TokenWithRefreshSchema containing access_token, token_type, and refresh_token.
   - Notes: Uses login_user service to verify credentials and generate tokens.

2. POST /auth/google
   - Purpose: Initiate Google OAuth2 authentication.
   - Input: None.
   - Output: Google OAuth2 authorization URL.
   - Notes: Uses get_google_auth service to generate the authorization URL.

3. POST /auth/google/callback
   - Purpose: Handle Google OAuth2 callback.
   - Input: HTTP Authorization header with Bearer <access_token>.
   - Output: TokenRefreshSchema containing access_token, token_type, and refresh_token.
   - Notes: Uses google_auth_callback service to handle the callback and generate tokens.
   
4. POST /auth/register
   - Purpose: Register a new user and generate authentication tokens.
   - Input: JSON body with 'username', 'email', and 'password' fields.
   - Output: TokenWithRefreshSchema containing access_token, token_type, and refresh_token.
   - Notes: Uses register_user service to create the user, assign the "user" role, and generate tokens.

5. POST /auth/logout
   - Purpose: Logout a user by invalidating their refresh token.
   - Input: HTTP Authorization header with Bearer <refresh_token>.
   - Output: JSON message confirming successful logout.
   - Notes: Uses logout service to remove the refresh token from the database.

Dependencies:
- db: SQLModel Session injected via Depends(get_db)
- logout_scheme: HTTPBearer for extracting refresh token from headers

In front-end after logout:
- Delete refresh token from localStorage
- Delete access token from localStorage
"""


# router - path prefix
router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)


# Authentication
@router.post(   # router path and response
    "/login",
    response_model=TokenRefreshSchema,
    summary="Authenticate a user",
    description="OAuth2 compatible login"
)
async def user_authentication(  # business logic
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    data = LoginSchema( # get form data
        username=form_data.username,
        password=form_data.password
    )
    return await login_user(db, data)

# Google Authentication

# OAuth
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

# http://localhost:8000/auth/google/login
@router.get("/google/login", response_model=None)
async def get_google_login(request: Request):
    return await get_google_auth(oauth, request)

@router.get("/google/callback", response_model=TokenRefreshSchema)
async def google_auth_handler(
    request: Request,
    db: Session = Depends(get_db),
):
    return await google_auth_callback(oauth, db, request)

# Registration
@router.post(   # router path and response
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

    register_user_with_token = await register_user(data, db)
    return register_user_with_token

# Logout
logout_scheme = HTTPBearer()    # take refresh token from header
@router.post(   # router path and response
    "/logout",
    summary="Logout a user", 
    description="Get JSON data and logout a user in the database"
)
async def logout_user(  # business logic
    data: Annotated[HTTPAuthorizationCredentials, Depends(logout_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    refresh_token = data.credentials
    return await logout(db, refresh_token)
