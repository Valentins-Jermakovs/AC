# Imports
from typing import Optional
from pydantic import BaseModel

# =============================
# SelectedProject schema - request
# =============================
class SelectedProject(BaseModel):
    workspaceId: str
    workspaceTitle: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "workspaceId": "workspaceId",
                    "workspaceTitle": "workspaceTitle"
                }
            ]
        }
    }