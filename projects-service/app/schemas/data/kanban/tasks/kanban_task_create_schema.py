# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskCreate schema for creating a new kanban task
# ============================================================
class KanbanTaskCreateSchema(BaseModel):
    board_id: str
    stage_id: str
    title: str
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "board_id": "board_id",
                    "stage_id": "stage_id",
                    "title": "Kanban task title",
                    "description": "Kanban task description"
                }
            ]
        }
    }