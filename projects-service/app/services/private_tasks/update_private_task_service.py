# Imports
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
# Models
from app.models import PrivateTaskModel
# Schemas
from app.schemas.response.private_tasks.private_task import PrivateTaskSchema
# Utils
from app.utils.time_converter import convert_to_datetime

# =======================
# Update private task
# =======================
async def update_private_task(
    task_id: str, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    dueDate: Optional[str] = None, 
    completed: Optional[bool] = None
) -> PrivateTaskSchema:
    
    # Raise if task id not provided
    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required")

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

        # Check title
        title = title.strip()

        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        
        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")
        
        # if title not unique
        if task.title == title:
            raise HTTPException(status_code=400, detail="Title must be unique")

    if description is not None:
        updated_data["description"] = description

        # Check description
        description = description.strip()

        if not description:
            raise HTTPException(status_code=400, detail="Description is required")
        
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        
        # if description not unique
        if task.description == description:
            raise HTTPException(status_code=400, detail="Description must be unique")

    if dueDate is not None:
        updated_data["dueDate"] = await convert_to_datetime(dueDate)

        # Check dueDate
        try:
            dueDate = await convert_to_datetime(dueDate)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if completed is not None:
        updated_data["completed"] = completed

        if not isinstance(completed, bool):
            raise HTTPException(status_code=400, detail="Completed must be a boolean")
    
        # if the same status
        if task.completed == completed:
            raise HTTPException(status_code=400, detail="Status must be different")

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

