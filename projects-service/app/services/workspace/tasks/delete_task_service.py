# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel


# ===============================
# Function delete task
# ================================
async def delete_task(
    task_id: str
) -> dict:

    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required")

    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # Get task
    task = await WorkspaceTaskModel.find_one({"_id": ObjectId(task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete task
    await task.delete()

    return {"message": f"Task '{task.title}' deleted successfully"}