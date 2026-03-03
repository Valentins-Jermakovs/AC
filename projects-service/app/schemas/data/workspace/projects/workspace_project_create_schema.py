# Imports
from pydantic import BaseModel
from typing import Optional

# =============================================================
# WorkspaceProjectCreate schema for creating a new workspace project
# =============================================================
class WorkspaceProjectCreateSchema(BaseModel):
    title: str
    description: Optional[str]
    # userId would be fetched from token

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "New project",
                    "description": "New project description"
                }
            ]
        }
    }