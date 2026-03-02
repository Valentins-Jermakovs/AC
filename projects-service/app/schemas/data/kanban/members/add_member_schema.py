# Imports
from pydantic import BaseModel

# ============================
# AddMember schema for adding a member
# ============================
class AddMemberSchema(BaseModel):
    user_id: str        # User ID
    board_id: str       # Board ID
    role: str           # Role

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "user_id",
                    "board_id": "board_id",
                    "role": "role"
                }
            ]
        }
    }