# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskUpdate schema for updating a kanban task
# ============================================================
class KanbanTaskUpdateSchema(BaseModel):
    taskId: str
    title: Optional[str] = None
    description: Optional[str] = None
    boardId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "task_id",
                    "title": "Kanban task title",
                    "description": "Kanban task description",
                    "boardId": "board_id"
                }
            ]
        }
    }