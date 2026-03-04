# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceCreateTask schema - request
# =============================
class WorkspaceCreateTaskSchema(BaseModel):
    project_id: str                       # Project ID
    stage_id: str                         # Stage ID
    title: str                            # Task title
    description: Optional[str] = None     # Task description
    story_points: int                     # Story points
    priority: int                         # Priority
    status: str                           # Status

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "stage_id": "stage_id",
                    "title": "New task",
                    "description": "New task description - optional",
                    "story_points": 1,
                    "priority": 1,
                    "status": "todo"
                }
            ]
        }
    }
