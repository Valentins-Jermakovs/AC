# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceUpdate  Task schema - request
# =============================
class WorkspaceUpdateTaskSchema(BaseModel):
    task_id: str
    title: Optional[str] = None            # Task title
    description: Optional[str] = None      # Task description
    story_points: Optional[int] = None     # Story points
    priority: Optional[int] = None         # Priority
    status: Optional[str] = None           # Status

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_id",
                    "title": "New task",
                    "description": "New task description - optional",
                    "story_points": 1,
                    "priority": 1,
                    "status": "todo"
                }
            ]
        }
    }
