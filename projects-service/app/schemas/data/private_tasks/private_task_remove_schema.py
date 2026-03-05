# Imports
from pydantic import BaseModel

# ============================================================
# PrivateTaskRemove schema for removing a private task
# ============================================================
class PrivateTaskRemoveSchema(BaseModel):
    taskId: str # The ID of the task to remove

    model_config = {
        "json_schema_extra": {
            "example": {
                "taskId": "1"
            }
        }
    }