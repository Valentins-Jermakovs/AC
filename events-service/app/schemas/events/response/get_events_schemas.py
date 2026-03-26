# Imports
from pydantic import BaseModel
from typing import Optional

# ============================================================
# Single event schema for getting a single event
# ============================================================
class SingleEventSchema(BaseModel):
    id: str
    title: str
    description: str
    creatorId: str
    startDate: str
    endDate: str
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    allDay: bool
    color: str
    status: str
    createdAt: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "event_id",
                    "title": "Event title",
                    "description": "Event description",
                    "creatorId": "creator_id",
                    "startDate": "2023-01-01",
                    "endDate": "2023-01-01",
                    "startTime": "00:00",
                    "endTime": "00:00",
                    "allDay": True,
                    "color": "primary",
                    "status": "active",
                    "createdAt": "2022-01-01"
                }
            ]
        }
    }

# ============================================================
# Pagination metadata schema for getting paginated events
# ============================================================
class PaginationMetadataSchema(BaseModel):
    page: int
    total_pages: int
    limit: int
    total_items: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "page": 1,
                    "total_pages": 10,
                    "limit": 10,
                    "total_items": 100
                }
            ]
        }
    }

# ============================================================
# Multiple events schema for getting multiple events
# ============================================================
class MultipleEventsSchema(BaseModel):
    events: list[SingleEventSchema]
    metadata: PaginationMetadataSchema

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "events": [
                        {
                            "id": "event_id",
                            "title": "Event title",
                            "description": "Event description",
                            "creatorId": "creator_id",
                            "startDate": "2023-01-01T00:00:00.000Z",
                            "endDate": "2023-01-01T00:00:00.000Z",
                            "allDay": True,
                            "color": "primary",
                            "status": "active",
                            "createdAt": "2022-01-01"
                        }
                    ],
                    "metadata": {
                        "page": 1,
                        "total_pages": 10,
                        "limit": 10,
                        "total_items": 100
                    }
                }
            ]
        }
    }

# ===========================================================
# Response schema for getting events in month
# ============================================================
class EventsInMonthSchema(BaseModel):
    events: list[SingleEventSchema]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "events": [
                        {
                            "id": "event_id",
                            "title": "Event title",
                            "description": "Event description",
                            "creatorId": "creator_id",
                            "startDate": "2023-01-01T00:00:00.000Z",
                            "endDate": "2023-01-01T00:00:00.000Z",
                            "allDay": True,
                            "color": "primary",
                            "status": "active",
                            "createdAt": "2022-01-01"
                        }
                    ]
                }
            ]
        }
    }