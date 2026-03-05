# Imports
from pydantic import BaseModel

# ============================================================
# KanbanTaskMoveBtwStages schema
# ============================================================
class KanbanTaskMoveBtwStagesSchema(BaseModel):
    taskId: str
    targetStageId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "taskId",
                    "targetStageId": "targetStageId"
                }
            ]
        }
    }