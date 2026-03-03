# Imports
from pydantic import BaseModel

# =============================================================
# WorkspaceProjectDelete schema for deleting a workspace project
# =============================================================
class WorkspaceProjectDeleteSchema(BaseModel):
    project_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id"
                }
            ]
        }
    }