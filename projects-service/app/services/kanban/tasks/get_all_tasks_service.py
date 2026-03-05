# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanTaskModel
# Schemas
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema

# ==================================
# Function get all tasks
# =================================
async def get_all_tasks(
    stage_id: str
) -> dict:
    
    # ===== Validation and error handling =====
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # ===== Business logic =====
    tasks = await KanbanTaskModel.find({
        "stageId": stage_id
    }).sort("order").to_list()

    # Build response
    items = [
        KanbanTaskSchema(
            id=str(task.id),
            title=task.title,
            description=task.description,
            order=task.order,
            stageId=task.stageId
        ) for task in tasks
    ]

    # Return response
    return {
        "items": items
    }
