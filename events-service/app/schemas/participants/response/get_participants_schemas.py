# Imports
from pydantic import BaseModel

# ===========================================================
# Single participant schema for getting a single participant
# ============================================================
class SingleParticipantSchema(BaseModel):
    id: str
    eventId: str
    userId: str
    userEmail: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "participant_id",
                    "eventId": "event_id",
                    "userId": "user_id",
                    "userEmail": "user_email"
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
# Multiple participants schema for getting all participants
# ============================================================
class MultipleParticipantsSchema(BaseModel):
    participants: list[SingleParticipantSchema]
    metadata: PaginationMetadataSchema

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "participants": [
                        {
                            "id": "participant_id",
                            "eventId": "event_id",
                            "userId": "user_id",
                            "userEmail": "user_email"
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