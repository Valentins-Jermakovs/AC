# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardCreate schema for creating a new kanban board
# ============================================================
class KanbanBoardUpdateSchema(BaseModel):
    board_id: str  # Kanban board ID
    title: str     # Kanban board title

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "board_id": "board_id",
                    "title": "Kanban board title"
                }
            ]
        }
    }