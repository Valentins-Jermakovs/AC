# Imports
from pydantic import BaseModel

# =============================
# WorkspaceProjectMembersGet schema - request
# =============================
class WorkspaceProjectMembersGetSchema(BaseModel):
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