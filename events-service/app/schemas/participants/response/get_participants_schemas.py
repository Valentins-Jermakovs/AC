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