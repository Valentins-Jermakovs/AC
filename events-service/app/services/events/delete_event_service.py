# Imports
from fastapi import HTTPException
from app.models import EventModel
from bson import ObjectId
# Models
from app.models.participants_models import ParticipantModel

# =================================
# Delete event
# =================================
async def delete_event(
    eventId: str,
    createrId: str
) -> dict:
    
    if not ObjectId.is_valid(eventId):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    event = await EventModel.find_one({
        "_id": ObjectId(eventId),
        "creatorId": createrId
    })

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete participants
    await ParticipantModel.find({
        "eventId": eventId
    }).delete()
    
    await event.delete()

    return {"message": "Event deleted successfully"}