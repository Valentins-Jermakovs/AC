# Imports
from pydantic import BaseModel

# =============================================================
# WorkspaceProjectDelete schema for deleting a workspace project
# =============================================================
class WorkspaceProjectDeleteSchema(BaseModel):
    projectId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId"
                }
            ]
        }
    }