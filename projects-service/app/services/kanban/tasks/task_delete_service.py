# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanTaskModel
# Schemas
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema

async def delete_task(
    task_id: str
) -> dict:

    # ===== Validation and error handling =====
    # Raise if task_id is not provided
    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required")
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # ===== Business logic =====
    # Get task
    task = await KanbanTaskModel.find_one({"_id": ObjectId(task_id)})
    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Delete task
    await task.delete()

    # Return success message
    return {"message": f"Task '{task.title}' deleted successfully"}