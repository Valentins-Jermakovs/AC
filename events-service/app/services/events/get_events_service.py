# Imports
# Schemas
from app.schemas.events.response.get_events_schemas import (
    SingleEventSchema,
    EventsInMonthSchema,
    MultipleEventsSchema,
    PaginationMetadataSchema
)
# Models
from app.models import EventModel
from app.models.participants_models import ParticipantModel
# Libraries
from fastapi import HTTPException
from bson import ObjectId

# ==========================
# Get all events
# ==========================
async def get_all_events(
    page: int = 1,
    limit: int = 10,
    user_id: int = None
):
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be 1-100")
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    # offset
    offset = (page - 1) * limit

    # get all events ids from participants collection
    participants = await ParticipantModel.find({
        "userId": user_id
    }).to_list()

    if not participants:
        return MultipleEventsSchema(
            events=[],
            metadata=PaginationMetadataSchema(
                page=0,
                total_pages=0,
                limit=limit,
                total_items=0
            )
        )

    # get all events from events collection by ids
    event_ids = [ObjectId(participant.eventId) for participant in participants]

    events = await EventModel.find({
        "_id": {"$in": event_ids}
    }).skip(offset).limit(limit).to_list()

    # total events
    total_events = len(participants)

    if not events:
        page = 0

    # metadata
    metadata = PaginationMetadataSchema(
        page=page,
        total_pages=(total_events + limit - 1) // limit,
        limit=limit,
        total_items=total_events
    )

    items = [
        SingleEventSchema(
            id=str(event.id),
            title=event.title,
            description=event.description,
            startDate=event.startDate.strftime("%Y-%m-%d"),
            endDate=event.endDate.strftime("%Y-%m-%d"),
            startTime=event.startTime,
            endTime=event.endTime,
            allDay=event.allDay,
            color=event.color,
            status=event.status,
            createdAt=event.createdAt.strftime("%Y-%m-%d")
        ) for event in events
    ]

    # return events
    return MultipleEventsSchema(
        events=items,
        metadata=metadata
    )
