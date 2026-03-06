# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel


# ===============================
# Function delete task
# ================================
async def delete_task(
    task_id: str,
    project_id: str,
    user_id: str
) -> dict:

    # ===== Validation and error handling =====

    # Check current user
    user =  await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    
    # Check if user is viewer
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")


    # Raise if task_id is not provided
    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required")
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # ===== Business logic =====
    # Get task
    task = await WorkspaceTaskModel.find_one({"_id": ObjectId(task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete task
    await task.delete()

    return {"message": f"Task '{task.title}' deleted successfully"}