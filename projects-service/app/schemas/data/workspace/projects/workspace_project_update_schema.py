# Imports
from pydantic import BaseModel
from typing import Optional

# ============================================================
# WorkspaceProjectUpdate schema for updating a workspace project
# ============================================================
class WorkspaceProjectUpdateSchema(BaseModel):
    project_id: str
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "title": "New project",
                    "description": "New project description - optional"
                }
            ]
        }
    }