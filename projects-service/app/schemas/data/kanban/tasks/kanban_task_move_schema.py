from pydantic import BaseModel

class KanbanTaskMoveSchema(BaseModel):
    task_id: str
    stage_id: str
    direction: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_id",
                    "stage_id": "stage_id",
                    "direction": "up"
                }
            ]
        }
    }