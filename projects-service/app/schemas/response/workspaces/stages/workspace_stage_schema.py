# Imports
from pydantic import BaseModel
from typing import Optional

# ===============================
# WorkspaceStageSchema schema - response
# ===============================
class WorkspaceStageSchema(BaseModel):
    id: str
    title: str
    description: Optional[str]
    project_id: str
    order: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "stage_id",
                    "title": "Stage title",
                    "description": "Stage description - optional",
                    "project_id": "project_id",
                    "order": 1000
                }
            ]
        }
    }