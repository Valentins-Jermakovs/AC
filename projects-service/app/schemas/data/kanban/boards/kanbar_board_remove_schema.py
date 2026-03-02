# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardRemove schema for removing a kanban board
# ============================================================
class KanbanBoardRemoveSchema(BaseModel):
    board_id: str   # The ID of the board

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "board_id": "board_id"
                }
            ]
        }
    }