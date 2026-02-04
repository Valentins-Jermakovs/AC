from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from ..dependencies.data_base_connection import get_db
from ..services.tokens_management.refresh_tokens_service import refresh_access_token, check_access_token
from ..schemas.tokens.token_refresh_schema import TokenRefreshSchema
from typing import Annotated
from sqlmodel import Session
# Refresh
refresh_scheme = HTTPBearer()   # take refresh token from header
access_scheme = HTTPBearer()    # take access token from header

router = APIRouter(
    prefix="/token", 
    tags=["Tokens check and refresh service"]
)

# Check access token
@router.get("/check", response_model=TokenRefreshSchema)
async def check_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(access_scheme)],
):
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=""
    )

# Refresh an access token
@router.post("/refresh", response_model=TokenRefreshSchema)
async def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(refresh_scheme)],
    db: Session = Depends(get_db)
):
    refresh_token = credentials.credentials
    return await refresh_access_token(refresh_token, db)