# Imports
from pydantic import BaseModel

# =============================
# RemoveKanbanBoardMember schema - request
# =============================

class RemoveKanbanBoardMemberSchema(BaseModel):
    userId: str      # Member ID
    boardId: str       # Board ID

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "userId": "userId",
                    "boardId": "boardId"
                }
            ]
        }
    }