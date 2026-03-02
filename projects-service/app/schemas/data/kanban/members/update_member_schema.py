# Imports
from pydantic import BaseModel

# =============================
# UpdateKanbanBoardMember schema - request
# =============================
class UpdateKanbanBoardMemberSchema(BaseModel):
    member_id: str        # User ID
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