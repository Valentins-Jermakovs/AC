# Imports
from pydantic import BaseModel
from typing import Optional

# ===========================================================
# UpdateEvent schema for updating an existing event
# ===========================================================
class UpdateEventSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    allDay: Optional[bool]
    color: Optional[str]
    status: Optional[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Event title",
                    "description": "Event description",
                    "startDate": "2023-01-01T00:00:00.000Z",
                    "endDate": "2023-01-01T00:00:00.000Z",
                    "allDay": True,
                    "color": "primary",
                    "status": "active"
                }
            ]
        }
    }