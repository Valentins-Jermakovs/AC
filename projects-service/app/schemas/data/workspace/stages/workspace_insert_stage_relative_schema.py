# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceInsertStageRelative schema - request
# =============================
class WorkspaceInsertStageRelativeSchema(BaseModel):
    projectId: str
    title: str
    description: Optional[str] = None
    referenceStageId: str
    position: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "title": "New stage",
                    "description": "New stage description - optional",
                    "referenceStageId": "stageId",
                    "position": "before | after"
                }
            ]
        }
    }