# Imports
from pydantic import BaseModel

# =============================
# WorkspaceMoveStage schema - request
# =============================
class WorkspaceMoveStageSchema(BaseModel):
    projectId: str
    stageId: str
    direction: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "stageId": "stageId",
                    "direction": "up"
                }
            ]
        }
    }