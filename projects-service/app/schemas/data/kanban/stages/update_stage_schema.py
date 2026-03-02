# Imports
from pydantic import BaseModel

# =============================
# UpdateKanbanStage schema - request
# =============================
class UpdateKanbanStageSchema(BaseModel):
    board_id: str
    stage_id: str
    title: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "board_id": "board_id",
                    "stage_id": "stage_id",
                    "title": "Kanban stage title"
                }
            ]
        }
    }