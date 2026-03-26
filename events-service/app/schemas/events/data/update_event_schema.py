# Imports
from pydantic import BaseModel
from typing import Optional

# ===========================================================
# UpdateEvent schema for updating an existing event
# ===========================================================
class UpdateEventSchema(BaseModel):
    eventId: str
    title: Optional[str]
    description: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    startTime: Optional[str]
    endTime: Optional[str]
    allDay: Optional[bool]
    color: Optional[str]
    status: Optional[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "eventId": "event_id",
                    "title": "Event title",
                    "description": "Event description",
                    "startDate": "2023-01-01",
                    "endDate": "2023-01-01",
                    "startTime": "00:00",
                    "endTime": "00:00",
                    "allDay": True,
                    "color": "primary",
                    "status": "active"
                }
            ]
        }
    }