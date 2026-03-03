# Imports
from pydantic import BaseModel

# =============================
# WorkspaceStageDelete schema - request
# =============================
class WorkspaceStageDelete(BaseModel):
    stage_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "stage_id": "stage_id"
                }
            ]
        }
    }