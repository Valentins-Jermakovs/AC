# Imports
from pydantic import BaseModel

# ===========================================================
# CreateParticipant schema for creating a new participant
# ===========================================================
class CreateParticipantSchema(BaseModel):
    eventId: str
    userId: str
    userEmail: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "eventId": "event_id",
                    "userId": "user_id",
                    "userEmail": "user_email"
                }
            ]
        }
    }