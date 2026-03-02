# Imports
from pydantic import BaseModel

# =============================
# RemoveKanbanBoardMember schema - request
# =============================

class RemoveKanbanBoardMemberSchema(BaseModel):
    member_id: str      # Member ID
    board_id: str       # Board ID

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "member_id": "member_id",
                    "board_id": "board_id"
                }
            ]
        }
    }