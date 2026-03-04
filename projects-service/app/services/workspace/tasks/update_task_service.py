# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel
# Schemas
# ===== response:
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema
# ===== data:
from app.schemas.data.workspace.tasks.workspace_update_task_schema import WorkspaceUpdateTaskSchema


# ===============================
# Function update task
# ================================
async def update_task(
    data: WorkspaceUpdateTaskSchema
) -> WorkspaceTaskSchema:
    # Raise if task_id is not valid
    if not ObjectId.is_valid(data.task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # Get task
    task = await WorkspaceTaskModel.find_one({"_id": ObjectId(data.task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Raise if task title already exists
    if await WorkspaceTaskModel.find_one({"title": data.title}):
        raise HTTPException(status_code=400, detail="Task title already exists")
    
    # Raise if task too short
    if len(data.title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # Raise if task too long
    if len(data.title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    # Raise if task description too long
    if len(data.description) > 1000:
        raise HTTPException(status_code=400, detail="Description is too long")
    
    # Raise if task description too short
    if len(data.description) < 3:
        raise HTTPException(status_code=400, detail="Description is too short")
    
    # Raise if description or title are the same
    if task.title == data.title or task.description == data.description:
        raise HTTPException(status_code=400, detail="Task is the same")

    # Update task
    task.title = data.title
    task.description = data.description
    task.story_points = data.story_points
    task.priority = data.priority
    task.status = data.status

    # Save task
    await task.save()

    return WorkspaceTaskSchema(
        id=str(task.id),
        project_id=str(task.projectId),
        stage_id=str(task.stageId),
        title=task.title,
        description=task.description,
        story_points=task.storyPoints,
        priority=task.priority,
        status=task.status
    )