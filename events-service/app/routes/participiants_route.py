# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== data:
from app.schemas.participants.data.create_participant_schema import CreateParticipantSchema
# ===== response:
from app.schemas.participants.response.get_participants_schemas import SingleParticipantSchema
# =========================
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.participants.create_participant_service import create_participant

# Router
router = APIRouter(
    prefix="/participants",
    tags=["Participants management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== POST ==========================================================
# Route for creating a new participant
@router.post(
    "/create-participant", 
    response_model=SingleParticipantSchema
)
async def create_participant_route(
    participant: CreateParticipantSchema, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new participant.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create participant in DB
    4. Return created participant
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_participant(
        data=participant
    )