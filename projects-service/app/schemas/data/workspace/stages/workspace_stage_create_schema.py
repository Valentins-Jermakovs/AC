# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceStageCreate schema - request
# =============================
class WorkspaceStageCreateSchema(BaseModel):
    projectId: str
    title: str
    description: Optional[str] = None
    dueDate: Optional[str] = None
    createdAt: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "project_id",
                    "title": "New stage",
                    "description": "New stage description - optional",
                    "dueDate": "2026-01-01",
                    "createdAt": "2022-01-01"
                }
            ]
        }
    }