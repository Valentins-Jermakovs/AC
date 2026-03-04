# Import
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceUpdate  Task schema - request
# =============================
class WorkspaceUpdateTaskSchema(BaseModel):
    title: Optional[str]            # Task title
    description: Optional[str]      # Task description
    story_points: Optional[int]     # Story points
    priority: Optional[int]         # Priority
    status: Optional[str]           # Status

    # Model config - examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "New task",
                    "description": "New task description - optional",
                    "story_points": 1,
                    "priority": 1,
                    "status": "todo"
                }
            ]
        }
    }
