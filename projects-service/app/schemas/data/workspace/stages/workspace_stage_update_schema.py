# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceStageUpdate schema - request
# =============================
class WorkspaceStageUpdateSchema(BaseModel):
    stage_id: str
    title: str
    description: Optional[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "stage_id": "stage_id",
                    "title": "New stage",
                    "description": "New stage description"
                }
            ]
        }
    }