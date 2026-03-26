# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== Events Schemas =====
# ===== data:
from app.schemas.events.data.create_event_schema import CreateEventSchema
# ===== response:
from app.schemas.events.response.get_events_schemas import SingleEventSchema
# =========================
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.events.create_event_service import create_event

# Router
router = APIRouter(
    prefix="/events",
    tags=["Events management service"]
)

# Security scheme for access token
security = HTTPBearer()


# ===== POST ==========================================================
@router.post(
    "/create-event",
    response_model=SingleEventSchema
)
async def create_event_endpoint(
    data: CreateEventSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a new event.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create event in DB
    4. Return created event
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await create_event(
        data=data, 
        user_id=user_id
    )