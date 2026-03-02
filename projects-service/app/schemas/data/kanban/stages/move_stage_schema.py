# Imports
from pydantic import BaseModel

# =============================
# MoveKanbanStage schema - request
# =============================
class MoveKanbanStageSchema(BaseModel):
    board_id: str
    stage_id: str
    direction: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "board_id": "board_id",
                    "stage_id": "stage_id",
                    "direction": "up"
                }
            ]
        }
    }