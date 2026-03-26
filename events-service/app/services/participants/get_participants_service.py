# Imports
# Models
from app.models import ParticipantModel, EventModel
# Schemas
from app.schemas.participants.response.get_participants_schemas import (
    SingleParticipantSchema,
    PaginationMetadataSchema,
    MultipleParticipantsSchema
)
# Libraries
from fastapi import HTTPException
from bson import ObjectId
from typing import List


# ================================
# Get all participants
# ================================
async def get_all_participants(
    page: int = 1,
    limit: int = 10,
    user_id: str = None,
    event_id: str | None = None
) -> MultipleParticipantsSchema:

    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be 1-100")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be positive")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID required")

    offset = (page - 1) * limit

    # if specific event requested
    if event_id:

        # validate ObjectId format
        if not ObjectId.is_valid(event_id):
            raise HTTPException(status_code=400, detail="Invalid event ID")

        event = await EventModel.find_one({
            "_id": ObjectId(event_id),
            "creatorId": str(user_id)
        })

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        query = {
            "eventId": event_id
        }

    else:

        events = await EventModel.find({
            "creatorId": str(user_id)
        }).to_list()

        if not events:
            return MultipleParticipantsSchema(
                participants=[],
                metadata=PaginationMetadataSchema(
                    page=1,
                    total_pages=0,
                    limit=limit,
                    total_items=0
                )
            )

        event_ids = [str(e.id) for e in events]

        query = {
            "eventId": {"$in": event_ids}
        }

    # total count
    total_items = await ParticipantModel.find(query).count()

    participants = await ParticipantModel.find(query)\
        .skip(offset)\
        .limit(limit)\
        .to_list()

    total_pages = (
        (total_items + limit - 1) // limit
        if total_items else 0
    )

    items = [
        SingleParticipantSchema(
            id=str(p.id),
            eventId=p.eventId,
            userId=p.userId,
            userEmail=p.userEmail
        )
        for p in participants
    ]

    return MultipleParticipantsSchema(
        participants=items,
        metadata=PaginationMetadataSchema(
            page=page,
            total_pages=total_pages,
            limit=limit,
            total_items=total_items
        )
    )