# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskCreate schema for creating a new kanban task
# ============================================================
class KanbanTaskCreateSchema(BaseModel):
    boardId: str
    stageId: str
    title: str
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardId": "boardId",
                    "stageId": "stageId",
                    "title": "Kanban task title",
                    "description": "Kanban task description"
                }
            ]
        }
    }