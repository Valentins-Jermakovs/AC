# Imports
from pydantic import BaseModel

# =============================
# WorkspaceDeleteTask schema - request
# =============================
class WorkspaceDeleteTaskSchema(BaseModel):
    task_id: str    # Task ID

    # Examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_id"
                }
            ]
        }
    }