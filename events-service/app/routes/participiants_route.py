# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== data:
from app.schemas.participants.data.create_participant_schema import CreateParticipantSchema
# ===== response:
from app.schemas.participants.response.get_participants_schemas import (
    SingleParticipantSchema,
    PaginationMetadataSchema,
    MultipleParticipantsSchema
)
# =========================
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.participants.create_participant_service import create_participant
from app.services.participants.delete_participant_service import delete_participant, leave_event
from app.services.participants.get_participants_service import get_all_participants, search_event_participants_by_email

# Router
router = APIRouter(
    prefix="/participants",
    tags=["Participants management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== GET ===========================================================
# Route for getting all participants
@router.get(
    "/get-all-participants",
    response_model=MultipleParticipantsSchema
)
async def get_all_participants_route(
    limit: int = 10,
    page: int = 1,
    event_id: str | None = None,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all participants.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all participants
    4. Return all participants
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_participants(
        limit=limit,
        page=page,
        user_id=user_id,
        event_id=event_id
    )

# Route for getting participants by email
@router.get(
    "/get-participants-by-email",
    response_model=MultipleParticipantsSchema
)
async def get_participants_by_email_route(
    email: str,
    event_id: str,
    limit: int = 10,
    page: int = 1,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get participants by email.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get participants by email
    4. Return participants
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await search_event_participants_by_email(
        event_id=event_id,
        email=email,
        user_id=user_id,
        page=page,
        limit=limit
    )

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

# ===== DELETE ==========================================================
# Route for deleting a participant
@router.delete(
    "/delete-participant/{eventId}/{userId}",
    response_model=dict
)
async def delete_participant_route(
    eventId: str,
    userId: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete a participant.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete participant in DB
    4. Return success message
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await delete_participant(
        eventId=eventId,
        userId=userId,
        operatorId=user_id
    )

# Route for leaving an event
@router.delete(
    "/leave-event/{eventId}",
    response_model=dict
)
async def leave_event_route(
    eventId: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Leave an event.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to leave event in DB
    4. Return success message
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await leave_event(
        eventId=eventId, 
        userId=user_id
    )