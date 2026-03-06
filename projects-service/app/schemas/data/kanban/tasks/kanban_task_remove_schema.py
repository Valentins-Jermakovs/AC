# Imports
from pydantic import BaseModel

# =============================================
# KanbanTaskRemove schema for removing a kanban task
# =============================================
class KanbanTaskRemoveSchema(BaseModel):
    taskId: str
    boardId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "taskId",
                    "boardId": "boardId"
                }
            ]
        }
    }