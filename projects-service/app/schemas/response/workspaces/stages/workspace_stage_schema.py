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
    projectId: str
    order: float
    dueDate: Optional[str]
    createdAt: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "stage_id",
                    "title": "Stage title",
                    "description": "Stage description - optional",
                    "projectId": "projectId",
                    "order": 1000,
                    "dueDate": "2026-01-01",
                    "createdAt": "2022-01-01"
                }
            ]
        }
    }