# Imports
from pydantic import BaseModel

# =============================
# KanbanStageCreateRelative schema - request
# =============================
class KanbanStageCreateRelativeSchema(BaseModel):
    reference_stage_id: str     # stage which will be used as reference
    board_id: str               # board ID
    title: str                  # stage title
    position: str               # "before" or "after"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "reference_stage_id": "stage_id",
                    "board_id": "board_id",
                    "title": "Kanban stage title",
                    "position": "before | after"
                }
            ]
        }
    }