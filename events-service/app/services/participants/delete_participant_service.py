from app.models import EventModel, ParticipantModel
from fastapi import HTTPException
from bson import ObjectId

async def delete_participant(
    eventId: str,
    userId: str,
    operatorId: str
) -> dict:
    
    if not ObjectId.is_valid(eventId):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    participant = await ParticipantModel.find_one({
        "eventId": eventId,
        "userId": userId
    })

    event = await EventModel.find_one({
        "_id": ObjectId(eventId),
        "creatorId": operatorId
    })

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # if non creator tries to delete
    if not event:
        raise HTTPException(status_code=403, detail="You are not the creator of this event")
    
    # if creator tries delete themselves
    if userId == operatorId:
        raise HTTPException(status_code=403, detail="You cannot delete yourself")

    await participant.delete()

    return {"message": "Participant deleted successfully"}