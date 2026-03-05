# Imports
from pydantic import BaseModel

# =============================
# KanbanStageCreateRelative schema - request
# =============================
class KanbanStageCreateRelativeSchema(BaseModel):
    referenceStageId: str     # stage which will be used as reference
    boardId: str               # board ID
    title: str                  # stage title
    position: str               # "before" or "after"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "referenceStageId": "stageId",
                    "boardId": "boardId",
                    "title": "Kanban stage title",
                    "position": "before | after"
                }
            ]
        }
    }