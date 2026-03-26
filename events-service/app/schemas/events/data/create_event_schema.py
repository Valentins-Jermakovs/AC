# Imports
from pydantic import BaseModel

# ===========================================================
# CreateEvent schema for creating a new event
# ===========================================================
class CreateEventSchema(BaseModel):
    title: str
    description: str
    startDate: str
    endDate: str
    allDay: bool
    color: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Event title",
                "description": "Event description",
                "startDate": "2023-01-01T00:00:00.000Z",
                "endDate": "2023-01-01T00:00:00.000Z",
                "allDay": True,
                "color": "primary",
                "status": "active"
            }
        }