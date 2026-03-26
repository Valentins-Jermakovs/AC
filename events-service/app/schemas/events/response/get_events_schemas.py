# Imports
from pydantic import BaseModel

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
    allDay: bool
    color: str
    status: str
    createdAt: str

    class Config:
        schema_extra = {
            "example": {
                "id": "event_id",
                "title": "Event title",
                "description": "Event description",
                "creatorId": "creator_id",
                "startDate": "2023-01-01T00:00:00.000Z",
                "endDate": "2023-01-01T00:00:00.000Z",
                "allDay": True,
                "color": "primary",
                "status": "active",
                "createdAt": "2023-01-01T00:00:00.000Z"
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

# ============================================================
# Multiple events schema for getting multiple events
# ============================================================
class MultipleEventsSchema(BaseModel):
    events: list[SingleEventSchema]
    metadata: PaginationMetadataSchema

# ===========================================================
# Response schema for getting events in month
# ============================================================
class EventsInMonthSchema(BaseModel):
    events: list[SingleEventSchema]