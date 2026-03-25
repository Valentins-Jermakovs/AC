# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceCreateTask schema - request
# =============================
class WorkspaceCreateTaskSchema(BaseModel):
    projectId: str                       # Project ID
    stageId: str                         # Stage ID
    title: str                            # Task title
    description: Optional[str] = None     # Task description
    storyPoints: int                     # Story points
    priority: int                         # Priority
    status: str                           # Status
    dueDate: Optional[str] = None
    createdAt: Optional[str] = None

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "stageId": "stageId",
                    "title": "New task",
                    "description": "New task description - optional",
                    "storyPoints": 1,
                    "priority": 1,
                    "status": "todo",
                    "dueDate": "2026-01-01",
                    "createdAt": "2022-01-01"
                }
            ]
        }
    }
