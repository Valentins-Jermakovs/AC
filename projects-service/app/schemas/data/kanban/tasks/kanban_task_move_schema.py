from pydantic import BaseModel

class KanbanTaskMoveSchema(BaseModel):
    taskId: str
    stageId: str
    direction: str
    boardId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "taskId": "taskId",
                    "stageId": "stageId",
                    "direction": "up",
                    "boardId": "boardId"
                }
            ]
        }
    }