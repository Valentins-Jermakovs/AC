# Imports
from pydantic import BaseModel

# =============================
# UpdateKanbanStage schema - request
# =============================
class UpdateKanbanStageSchema(BaseModel):
    boardId: str
    stageId: str
    title: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardId": "boardId",
                    "stageId": "stageId",
                    "title": "Kanban stage title"
                }
            ]
        }
    }