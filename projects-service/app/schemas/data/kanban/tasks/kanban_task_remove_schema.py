# Imports
from pydantic import BaseModel

# =============================================
# KanbanTaskRemove schema for removing a kanban task
# =============================================
class KanbanTaskRemoveSchema(BaseModel):
    task_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_id"
                }
            ]
        }
    }