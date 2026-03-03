# Imports
from pydantic import BaseModel

# =============================
# WorkspaceGetAllStages schema - request
# =============================
class WorkspaceGetAllStagesSchema(BaseModel):
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