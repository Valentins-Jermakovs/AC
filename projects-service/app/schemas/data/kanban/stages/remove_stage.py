# Imports
from pydantic import BaseModel

# =============================
# RemoveKanbanStage schema - request
# =============================
class RemoveKanbanStage(BaseModel):
    stageId: str
    boardId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "stageId": "stageId",
                    "boardId": "boardId"
                }
            ]
        }
    }