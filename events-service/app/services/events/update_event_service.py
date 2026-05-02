# Imports
# Schemas
from app.schemas.events.response.get_events_schemas import SingleEventSchema
from app.schemas.events.data.update_event_schema import UpdateEventSchema
# Models
from app.models import EventModel
from app.models.events_models import ColorEnum, StatusEnum
from app.models.participants_models import ParticipantModel
from bson import ObjectId
# Libraries
from fastapi import HTTPException
from datetime import datetime, timezone
# Utilities
from app.utils.current_date import get_current_date
from app.utils.time_converter import convert_to_datetime


# ===========================
# Update event
# ===========================
async def update_event(
    data: UpdateEventSchema,
    user_id: str
) -> SingleEventSchema:
    # Check is current user is creator?
    creator = await EventModel.find_one({
        "creatorId": user_id
    })

    if not creator:
        raise HTTPException(status_code=403, detail="You are not the creator of this event")
    
    # ===== Validation =====
    # Check if start date is before end date
    start_date = await convert_to_datetime(data.startDate) if data.startDate else None
    end_date = await convert_to_datetime(data.endDate) if data.endDate else None

    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    
    if start_date and start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date and end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)

    today = get_current_date().date()
        
    # Check title uniqueness except for current event
    if await EventModel.find_one({
        "title": data.title,
        "creatorId": user_id,
        "_id": {"$ne": ObjectId(data.eventId)}
    }):
        raise HTTPException(status_code=400, detail="Event with this title already exists")
    # Validate title length
    if data.title and not (3 <= len(data.title) <= 100):
        raise HTTPException(status_code=400, detail="Title must be between 3 and 100 characters")
    # Validate description length
    if data.description and not (3 <= len(data.description) <= 1000):
        raise HTTPException(status_code=400, detail="Description must be between 3 and 1000 characters")
        
    # Check if start time and end time are valid
    if data.startTime:
        try:
            datetime.strptime(data.startTime, "%H:%M")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start time format. Use HH:MM")
    if data.endTime:
        try:
            datetime.strptime(data.endTime, "%H:%M")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end time format. Use HH:MM")
    
    # ===== Update event =====
        
    event = await EventModel.find_one({
        "_id": ObjectId(data.eventId),
        "creatorId": user_id
    })

    print("EventId:", data.eventId, "Type:", type(data.eventId))
    print("UserId:", user_id, "Type:", type(user_id))

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if data.status:
        try:
            event.status = StatusEnum(data.status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")

    if data.color:
        try:
            event.color = ColorEnum(data.color)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid color")
        
    # Update event
    event.title = data.title if data.title else event.title
    event.description = data.description if data.description else event.description
    event.startDate = start_date if start_date else event.startDate
    event.endDate = end_date if end_date else event.endDate
    event.startTime = data.startTime if data.startTime else event.startTime
    event.endTime = data.endTime if data.endTime else event.endTime
    event.allDay = data.allDay if data.allDay is not None else event.allDay

    await event.save()

    return SingleEventSchema(
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