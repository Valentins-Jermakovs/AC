# Imports
from pydantic import BaseModel

# =============================
# WorkspaceStageDelete schema - request
# =============================
class WorkspaceStageDelete(BaseModel):
    stageId: str
    projectId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "stageId": "stageId",
                    "projectId": "projectId"
                }
            ]
        }
    }