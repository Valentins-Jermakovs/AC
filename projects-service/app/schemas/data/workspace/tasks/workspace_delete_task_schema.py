# Imports
from pydantic import BaseModel

# =============================
# WorkspaceDeleteTask schema - request
# =============================
class WorkspaceDeleteTaskSchema(BaseModel):
    taskId: str    # Task ID
    projectId: str

    # Examples
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "taskId",
                    "projectId": "projectId"
                }
            ]
        }
    }