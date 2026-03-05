# Imports
from pydantic import BaseModel
from typing import Optional

# ============================================================
# WorkspaceProjectUpdate schema for updating a workspace project
# ============================================================
class WorkspaceProjectUpdateSchema(BaseModel):
    projectId: str
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "title": "New project",
                    "description": "New project description - optional"
                }
            ]
        }
    }