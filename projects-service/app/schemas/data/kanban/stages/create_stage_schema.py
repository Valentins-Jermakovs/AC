# Imports
from pydantic import BaseModel

# =============================
# KanbanStageCreate schema - request
# =============================
class CreateKanbanStageSchema(BaseModel):
    title: str      # Title of the stage
    boardId: str   # ID of the board

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Kanban stage title",
                    "boardId": "boardId"
                }
            ]
        }
    }