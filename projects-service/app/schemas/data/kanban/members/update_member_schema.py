# Imports
from pydantic import BaseModel

# =============================
# UpdateKanbanBoardMember schema - request
# =============================
class UpdateKanbanBoardMemberSchema(BaseModel):
    userId: str        # User ID
    boardId: str       # Board ID
    role: str           # Role

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "userId": "userId",
                    "boardId": "boardId",
                    "role": "role"
                }
            ]
        }
    }