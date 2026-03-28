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
from datetime import datetime, timezone
from bson import ObjectId
import re

# ==========================
# Get all events
# ==========================
async def get_all_events(
    page: int = 1,
    limit: int = 10,
    user_id: int = None
) -> MultipleEventsSchema:
    
    if page < 1:
        page = 1

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

# Get all events in a month
async def get_all_events_in_month(
    month: int, 
    year: int,
    user_id: str
) -> EventsInMonthSchema:
    if year < 1:
        raise HTTPException(status_code=400, detail="Invalid year")

    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")

    start_date = datetime(year, month, 1, tzinfo=timezone.utc)

    if month == 12:
        end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_date = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    participants = await ParticipantModel.find({
        "userId": user_id
    }).to_list()

    if not participants:
        return EventsInMonthSchema(events=[])

    event_ids = [
        ObjectId(p.eventId)
        for p in participants
        if ObjectId.is_valid(p.eventId)
    ]

    calendar_events = await EventModel.find({
        "_id": {"$in": event_ids},
        "startDate": {"$lt": end_date},
        "endDate": {"$gte": start_date}
    }).to_list()

    events = [
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
        ) for event in calendar_events
    ]

    return EventsInMonthSchema(events=events)


# Get events by title
async def get_events_by_title(
    title: str,
    user_id: str,
    page: int = 1,
    limit: int = 10
):

    # validate pagination
    if page < 1:
        page = 1

    if limit < 1 or limit > 100:
        limit = 10

    # get participant events
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

    # safe ObjectId conversion
    event_ids = [
        ObjectId(p.eventId)
        for p in participants
        if ObjectId.is_valid(p.eventId)
    ]

    if not event_ids:
        return MultipleEventsSchema(
            events=[],
            metadata=PaginationMetadataSchema(
                page=0,
                total_pages=0,
                limit=limit,
                total_items=0
            )
        )

    # safe regex search
    safe_title = re.escape(title.strip())

    query = {
        "_id": {"$in": event_ids},
        "title": {
            "$regex": safe_title,
            "$options": "i"
        }
    }

    # count FIRST
    total_events = await EventModel.find(query).count()

    total_pages = (
        (total_events + limit - 1) // limit
        if total_events else 0
    )

    # clamp page
    if total_pages == 0:
        page = 0
    elif page > total_pages:
        page = total_pages

    skip = (page - 1) * limit if page > 0 else 0

    # get events
    events = await EventModel.find(query)\
        .sort("-createdAt")\
        .skip(skip)\
        .limit(limit)\
        .to_list()

    # map response
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
        )
        for event in events
    ]

    return MultipleEventsSchema(
        events=items,
        metadata=PaginationMetadataSchema(
            page=page,
            total_pages=total_pages,
            limit=limit,
            total_items=total_events
        )
    )