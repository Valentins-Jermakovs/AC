# Imports
from pydantic import BaseModel

# =============================
# RemoveKanbanStage schema - request
# =============================
class RemoveKanbanStage(BaseModel):
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