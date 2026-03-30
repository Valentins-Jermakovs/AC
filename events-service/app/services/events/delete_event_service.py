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
    creatorId: str
) -> dict:
    
    # Check is current user is creator?
    creator = await EventModel.find_one({
        "creatorId": creatorId
    })

    if not creator:
        raise HTTPException(status_code=403, detail="You are not the creator of this event")
    
    
    if not ObjectId.is_valid(eventId):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    event = await EventModel.find_one({
        "_id": ObjectId(eventId),
        "creatorId": creatorId
    })

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete participants
    await ParticipantModel.find({
        "eventId": eventId
    }).delete()
    
    await event.delete()

    return {"message": "Event deleted successfully"}