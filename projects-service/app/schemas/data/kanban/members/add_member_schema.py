# Imports
from pydantic import BaseModel

# ============================
# AddMember schema for adding a member
# ============================
class AddMemberSchema(BaseModel):
    userId: str        # User ID
    boardId: str       # Board ID
    role: str           # Role

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "userId": "userId",
                    "boardId": "boardId",
                    "role": "viewer | editor | admin"
                }
            ]
        }
    }