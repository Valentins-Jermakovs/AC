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
    startTime: str
    endTime: str
    allDay: bool
    color: str
    status: str
    creatorEmail: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Event title",
                    "description": "Event description",
                    "startDate": "2023-01-01",
                    "endDate": "2023-01-01",
                    "startTime": "00:00",
                    "endTime": "00:00",
                    "allDay": True,
                    "color": "primary",
                    "status": "active",
                    "creatorEmail": "Ig0wz@example.com"
                }
            ]
        }
    }