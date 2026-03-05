# Imports
from pydantic import BaseModel

# =============================
# MoveKanbanStage schema - request
# =============================
class MoveKanbanStageSchema(BaseModel):
    boardId: str
    stageId: str
    direction: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardId": "boardId",
                    "stageId": "stageId",
                    "direction": "up"
                }
            ]
        }
    }