# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceInsertStageRelative schema - request
# =============================
class WorkspaceInsertStageRelativeSchema(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    reference_stage_id: str
    position: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "title": "New stage",
                    "description": "New stage description - optional",
                    "reference_stage_id": "stage_id",
                    "position": "before"
                }
            ]
        }
    }