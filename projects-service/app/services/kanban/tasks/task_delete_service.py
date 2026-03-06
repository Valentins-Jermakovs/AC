# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanTaskModel, KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema

async def delete_task(
    task_id: str,
    user_id: str,
    board_id: str
) -> dict:

    # ===== Validation and error handling =====
    # Raise if task_id is not provided
    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required")
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # ===== Current user handling =====
    # Check role of current user
    user = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this board or this board does not exist")
    
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot create stage in this board")
    
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