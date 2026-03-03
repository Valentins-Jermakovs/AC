# Imports
from pydantic import BaseModel

# =============================
# WorkspaceMoveStage schema - request
# =============================
class WorkspaceMoveStageSchema(BaseModel):
    project_id: str
    stage_id: str
    direction: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "stage_id": "stage_id",
                    "direction": "up"
                }
            ]
        }
    }