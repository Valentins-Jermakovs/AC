# Imports
from fastapi import HTTPException
from app.models import EventModel
from bson import ObjectId

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
    
    await event.delete()

    return {"message": "Event deleted successfully"}