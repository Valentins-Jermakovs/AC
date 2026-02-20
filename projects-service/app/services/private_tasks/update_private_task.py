# Imports
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
# Models
from ...models import PrivateTaskModel
# Schemas
from ...schemas.response.private_task import PrivateTaskSchema

async def update_private_task(
    task_id: str, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    dueDate: Optional[str] = None, 
    completed: Optional[bool] = None
):
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # Get task
    task = await PrivateTaskModel.find_one({"_id": ObjectId(task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = {}   # Dictionary to store updated data

    # ===== Update data =====
    if title is not None:
        updated_data["title"] = title

    if description is not None:
        updated_data["description"] = description

    if dueDate is not None:
        updated_data["dueDate"] = dueDate

    if completed is not None:
        updated_data["completed"] = completed

    # ===== Update task =====
    
    if updated_data:
        await task.set(updated_data)

    return PrivateTaskSchema(
        id=str(task.id),              # ObjectId -> str
        title=task.title,
        description=task.description,
        createdAt=task.createdAt,
        dueDate=task.dueDate,
        completed=task.completed
    )

