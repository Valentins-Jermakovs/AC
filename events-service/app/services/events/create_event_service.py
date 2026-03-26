# Imports
# Schemas
from app.schemas.events.response.get_events_schemas import SingleEventSchema
from app.schemas.events.data.create_event_schema import CreateEventSchema
# Models
from app.models import EventModel
from app.models.events_models import ColorEnum, StatusEnum
# Utilities
from app.utils.current_date import get_current_date
from app.utils.time_converter import convert_to_datetime
# Libraries
from fastapi import HTTPException
from datetime import datetime, timezone

async def create_event(
    data: CreateEventSchema,
    user_id: str
) -> SingleEventSchema:
  
    # ===== Validation =====
    # Check if start date is before end date
    start_date = await convert_to_datetime(data.startDate)
    end_date = await convert_to_datetime(data.endDate)
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")
  
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)

    # Check if start date is in the past
    if start_date < get_current_date():
        raise HTTPException(status_code=400, detail="Start date cannot be in the past")
  
    # Check if end date is in the past
    if end_date < get_current_date():
        raise HTTPException(status_code=400, detail="End date cannot be in the past")
  
    # Check title uniqueness
    if await EventModel.find_one({
        "title": data.title,
        "creatorId": user_id
    }):
        raise HTTPException(status_code=400, detail="Event title already exists")
    # Validate title length
    if not (3 <= len(data.title) <= 100):
        raise HTTPException(status_code=400, detail="Title must be between 3 and 100 characters")
    # Validate description length
    if data.description and not (3 <= len(data.description) <= 1000):
        raise HTTPException(status_code=400, detail="Description must be between 3 and 1000 characters")

    # Validate status and color in enums
    try:
        status_enum = StatusEnum(data.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    try:
        color_enum = ColorEnum(data.color)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid color")
    
    # Validate startTime and endTime format for HH:MM
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

    # ===== Create event =====
    event = EventModel(
        title=data.title,
        description=data.description,
        creatorId=user_id,
        startDate=start_date,
        endDate=end_date,
        startTime=data.startTime,
        endTime=data.endTime,
        allDay=data.allDay,
        color=color_enum,
        status=status_enum,
        createdAt=get_current_date()
    )

    await event.save()

    return SingleEventSchema(
        id=str(event.id),
        title=event.title,
        description=event.description,
        creatorId=event.creatorId,
        startDate=event.startDate.strftime("%Y-%m-%d"),
        endDate=event.endDate.strftime("%Y-%m-%d"),
        startTime=event.startTime,
        endTime=event.endTime,
        allDay=event.allDay,
        color=event.color,
        status=event.status,
        createdAt=event.createdAt.strftime("%Y-%m-%d")
    )
 