# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceUpdate  Task schema - request
# =============================
class WorkspaceUpdateTaskSchema(BaseModel):
    taskId: str
    title: Optional[str] = None            # Task title
    description: Optional[str] = None      # Task description
    storyPoints: Optional[int] = None     # Story points
    priority: Optional[int] = None         # Priority
    status: Optional[str] = None           # Status

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "task_id",
                    "title": "New task",
                    "description": "New task description - optional",
                    "storyPoints": 1,
                    "priority": 1,
                    "status": "todo"
                }
            ]
        }
    }
