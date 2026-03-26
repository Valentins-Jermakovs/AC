# Imports
# Schemas
from app.schemas.participants.response.get_participants_schemas import SingleParticipantSchema
from app.schemas.participants.data.create_participant_schema import CreateParticipantSchema
# Models
from app.models import ParticipantModel
# Libraries
from fastapi import HTTPException
from bson import ObjectId
import re

# ================================
# Create participant
# ================================
async def create_participant(
    data: CreateParticipantSchema
) -> SingleParticipantSchema:
    # ===== Validation =====
    # validate event id
    if not ObjectId.is_valid(data.eventId):
        raise HTTPException(status_code=400, detail="Invalid event ID")
    # validate email with regex
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data.userEmail):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    # ===== Check if participant already exists =====
    if await ParticipantModel.find_one({
        "eventId": data.eventId,
        "userEmail": data.userEmail
    }):
        raise HTTPException(status_code=400, detail="Participant already exists")

    # ===== Create participant =====
    participant = ParticipantModel(
        eventId=data.eventId,
        userId=data.userId,
        userEmail=data.userEmail
    )

    # ===== Save participant =====
    await participant.save()

    return SingleParticipantSchema(
        id=str(participant.id),
        eventId=data.eventId,
        userId=data.userId,
        userEmail=data.userEmail
    )