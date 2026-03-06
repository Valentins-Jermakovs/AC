# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceStageUpdate schema - request
# =============================
class WorkspaceStageUpdateSchema(BaseModel):
    stageId: str
    projectId: str
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "stageId": "stageId",
                    "projectId": "projectId",
                    "title": "New stage",
                    "description": "New stage description"
                }
            ]
        }
    }