# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceUpdate  Task schema - request
# =============================
class WorkspaceUpdateTaskSchema(BaseModel):
    taskId: str
    projectId: str
    title: Optional[str] = None            # Task title
    description: Optional[str] = None      # Task description
    storyPoints: Optional[int] = None     # Story points
    priority: Optional[int] = None         # Priority
    status: Optional[str] = None           # Status
    dueDate: Optional[str] = None

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "project_id",
                    "taskId": "task_id",
                    "title": "New task",
                    "description": "New task description - optional",
                    "storyPoints": 1,
                    "priority": 1,
                    "status": "todo",
                    "dueDate": "2026-01-01"
                }
            ]
        }
    }
