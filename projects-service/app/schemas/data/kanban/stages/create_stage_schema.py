# Imports
from pydantic import BaseModel

# =============================
# KanbanStageCreate schema - request
# =============================
class CreateKanbanStageSchema(BaseModel):
    tilte: str      # Title of the stage
    board_id: str   # ID of the board

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Kanban stage title",
                    "board_id": "board_id"
                }
            ]
        }
    }