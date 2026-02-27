# =========================
# Tokens check and refresh service
# =========================

# Imports
from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from typing import Annotated
from sqlmodel import Session
# Services
from ..services.tokens_management.refresh_tokens_service import refresh_access_token, check_access_token
# Schemas
from ..schemas.tokens.token_refresh_schema import TokenRefreshSchema
# Dependencies
from ..dependencies.data_base_connection import get_db



# =========================
# Router setup
# =========================
router = APIRouter(
    prefix="/token",                            # All endpoints start with /token
    tags=["Tokens check and refresh service"]   # Tag for docs grouping
)


# Security schemes for extracting tokens from headers
refresh_scheme = HTTPBearer()   # For refresh token
access_scheme = HTTPBearer()    # For access token


# =========================
# Check access token endpoint
# =========================
@router.get("/check", response_model=TokenRefreshSchema)
async def check_token_endpoint(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(access_scheme)],
):
    """
    Validate the access token.

    Steps:
    1. Extract access token from header
    2. Verify token and get user ID
    3. Return the same access token and empty refresh token
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=""    # No refresh token returned in this endpoint
    )


# =========================
# Refresh access token endpoint
# =========================
@router.post("/refresh", response_model=TokenRefreshSchema)
async def refresh_token_endpoint(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(refresh_scheme)],
    db: Session = Depends(get_db)
):
    """
    Generate a new access token using a refresh token.

    Steps:
    1. Extract refresh token from header
    2. Verify token and generate new access token
    3. Return new access and refresh tokens
    """
    refresh_token = credentials.credentials
    return await refresh_access_token(refresh_token, db)