# Imports
from pydantic import BaseModel

# ============================================================
# KanbanTaskMoveBtwStages schema
# ============================================================
class KanbanTaskMoveBtwStagesSchema(BaseModel):
    task_id: str
    target_stage_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_id",
                    "target_stage_id": "target_stage_id"
                }
            ]
        }
    }