# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardRemove schema for removing a kanban board
# ============================================================
class KanbanBoardRemoveSchema(BaseModel):
    boardId: str   # The ID of the board

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardId": "boardId"
                }
            ]
        }
    }