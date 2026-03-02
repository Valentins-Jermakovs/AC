# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardCreate schema for creating a new kanban board
# ============================================================
class KanbanBoardCreateSchema(BaseModel):
    title: str  # Kanban board title

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Kanban board title"
                }
            ]
        }
    }