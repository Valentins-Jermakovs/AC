# Imports
from pydantic import BaseModel
from typing import Optional

# ===========================================================
# PrivateTaskUpdate schema for updating a private task
# ===========================================================
class PrivateTaskUpdateSchema(BaseModel):
    taskId: str
    title: Optional[str] = None         # Task title
    description: Optional[str] = None   # Task description
    dueDate: Optional[str] = None       # Task due date
    completed: Optional[bool] = None    # Task completion

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "taskId",
                    "title": "New task",
                    "description": "New task description",
                    "dueDate": "2023-01-01",
                    "completed": True
                }
            ]
        }
    }