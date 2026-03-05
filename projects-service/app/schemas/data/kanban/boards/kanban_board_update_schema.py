# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardCreate schema for creating a new kanban board
# ============================================================
class KanbanBoardUpdateSchema(BaseModel):
    boardId: str  # Kanban board ID
    title: str     # Kanban board title

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardId": "boardId",
                    "title": "Kanban board title"
                }
            ]
        }
    }