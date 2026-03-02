# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from ...models import KanbanTaskModel
# Schemas
from ...schemas.response.kanban_task import KanbanTaskSchema

async def delete_task(task_id: str):
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # Get task
    task = await KanbanTaskModel.find_one({"_id": ObjectId(task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete task
    await task.delete()

    return {"message": f"Task '{task.title}' deleted successfully"}