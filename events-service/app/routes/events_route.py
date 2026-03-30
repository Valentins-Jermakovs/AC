# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== Events Schemas =====
# ===== data:
from app.schemas.events.data.create_event_schema import CreateEventSchema
from app.schemas.events.data.update_event_schema import UpdateEventSchema
# ===== response:
from app.schemas.events.response.get_events_schemas import SingleEventSchema
from app.schemas.events.response.get_events_schemas import (
    MultipleEventsSchema,
    EventsInMonthSchema
)
# =========================
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.events.create_event_service import create_event
from app.services.events.delete_event_service import delete_event
from app.services.events.update_event_service import update_event
from app.services.events.get_events_service import (
    get_all_events,
    get_all_events_in_month,
    get_events_by_title,
    is_creator_of_event
)

# Router
router = APIRouter(
    prefix="/events",
    tags=["Events management service"]
)

# Security scheme for access token
security = HTTPBearer()


# ===== GET ===========================================================
@router.get(
    "/get-all-events",
    response_model=MultipleEventsSchema
)
async def get_all_events_endpoint(
    credantials: HTTPAuthorizationCredentials = Depends(security),
    limit: int = 10,
    page: int = 1
):
    """
    Get all events.

    Steps:
    1. Call service to get all events in DB
    2. Return all events
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_events(
        page=page,
        limit=limit,
        user_id=user_id
    )


@router.get(
    "/get-all-events-in-month",
    response_model=EventsInMonthSchema
)
async def get_all_events_in_month_endpoint(
    month: int,
    year: int,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all events in a month.

    Steps:
    1. Call service to get all events in DB
    2. Return all events
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_events_in_month(
        month=month,
        year=year,
        user_id=user_id
    )


@router.get(
    "/get-events-by-title",
    response_model=MultipleEventsSchema
)
async def get_events_by_title_endpoint(
    title: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all events by title.

    Steps:
    1. Call service to get all events in DB
    2. Return all events
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_events_by_title(
        title=title,
        page=page,
        limit=limit,
        user_id=user_id
    )

@router.get(
    "/is-creator-of-event",
    response_model=bool
)
async def is_creator_of_event_endpoint(
    event_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all events by title.

    Steps:
    1. Call service to get all events in DB
    2. Return all events
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await is_creator_of_event(
        event_id=event_id,
        user_id=user_id
    )

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

# ===== PUT =============================================================
@router.put(
    "/update-event",
    response_model=SingleEventSchema
)
async def update_event_endpoint(
    data: UpdateEventSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update an event.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update event in DB
    4. Return updated event
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_event(
        data=data,
        user_id=user_id
    )

# ===== DELETE ==========================================================
@router.delete(
    "/delete-event/{eventId}",
    response_model=dict
)
async def delete_event_endpoint(
    eventId: str,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Delete an event.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete event in DB
    4. Return success message
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await delete_event(
        eventId=eventId, 
        creatorId=user_id
    )