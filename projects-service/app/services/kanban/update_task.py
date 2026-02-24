# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from ...models import KanbanTaskModel
# Schemas
from ...schemas.response.kanban_task import KanbanTaskSchema


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
):
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
        updated_data["title"] = title

    # If task new description exist
    if description is not None and description != task.description:
        updated_data["description"] = description

    if not updated_data:
        raise HTTPException(status_code=400, detail="No data to update")

    await task.set(updated_data)

    # Return task
    return KanbanTaskSchema(
        id=str(task.id),
        title=task.title,
        description=task.description
    )