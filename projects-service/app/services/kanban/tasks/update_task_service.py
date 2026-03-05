# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from app.models import KanbanTaskModel
# Schemas
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema


# Function update task
# Parameters:
# - task_id: The ID of the task to update
# - title: The new title of the task
# - description: The new description of the task
# Returns:
# - The updated task
async def update_task(
    task_id: str, 
    title: Optional[str] = None, 
    description: Optional[str] = None,
) -> KanbanTaskSchema:
    
    # ===== Validation and error handling =====
    # Raise if task_id is not valid
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    # Get task
    task = await KanbanTaskModel.find_one({"_id": ObjectId(task_id)})
    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_data = {}

    # If task new title exist
    if title is not None and title != task.title:
        # task unique title
        if await KanbanTaskModel.find_one({"title": title}):
            raise HTTPException(status_code=400, detail="Task title already exists")
        # Check title
        title = title.strip()
        # Raise if title is empty
        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        # Raise if title is too short
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")
        # Update title
        updated_data["title"] = title

    # If task new description exist
    if description is not None and description != task.description:
        # Check description
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        # Update description
        updated_data["description"] = description
    # Raise if no data to update
    if not updated_data:
        raise HTTPException(status_code=400, detail="No data to update")

    # ===== Update task =====

    # Update task
    await task.set(updated_data)

    # Return task
    return KanbanTaskSchema(
        id=str(task.id),
        title=task.title,
        description=task.description,
        stageId=task.stageId,
        order=task.order
    )