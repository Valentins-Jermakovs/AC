# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceStageCreate schema - request
# =============================
class WorkspaceStageCreateSchema(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "title": "New stage",
                    "description": "New stage description - optional"
                }
            ]
        }
    }