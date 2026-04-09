# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utilities
from app.utils.check_access_token import check_access_token
# Services
from app.services.session_end_service import end_session
from app.services.session_start_service import start_session
from app.services.visit_registration_service import register_visit
from app.services.weekly_stats_service import get_week_stats

# =========================
# ROUTER SETUP
# =========================
router = APIRouter(
    prefix="/visit",
    tags=["Visit management service"]
)

# Authentication dependency using HTTP Bearer token
security = HTTPBearer()

# =========================
# ROUTES
# =========================
@router.post("/register")
async def register_visit_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Register a visit for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `register_visit` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await register_visit(user_id=user_id)


@router.post("/start")
async def start_session_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Start a new session for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `start_session` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await start_session(user_id=user_id)


@router.post("/end")
async def end_session_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    End the current user's session.

    - Requires authentication
    - Validates user via access token
    - Uses `end_session` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await end_session(user_id=user_id)


@router.get("/stats")
async def get_week_stats_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get weekly statistics for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `get_week_stats` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_week_stats(user_id=user_id)