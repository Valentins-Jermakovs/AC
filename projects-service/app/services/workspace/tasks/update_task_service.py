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
    
    if data.title is not None:
        
        # Raise if task title already exists
        if await WorkspaceTaskModel.find_one({"title": data.title, "_id": {"$ne": task.id}}):
            raise HTTPException(status_code=400, detail="Task title already exists")
    
        # Raise if task too short
        if len(data.title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")
        
        # Raise if task too long
        if len(data.title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        
        task.title = data.title


    if data.description is not None:
        # Raise if task description too long
        if len(data.description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
    
        # Raise if task description too short
        if len(data.description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        
        task.description = data.description

    if data.story_points is not None:

        if data.story_points not in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
            raise HTTPException(status_code=400, detail="Story points must be between 1 and 9")
        
        task.storyPoints = data.story_points

    if data.priority is not None:

        if data.priority not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")

        task.priority = data.priority

    if data.status is not None:

        if data.status not in ["todo", "in_progress", "done"]:
            raise HTTPException(status_code=400, detail="Status must be todo, in_progress or done")

        task.status = data.status

    # Save task
    await task.save()

    return WorkspaceTaskSchema(
        id=str(task.id),
        projectId=str(task.projectId),
        stageId=str(task.stageId),
        title=task.title,
        description=task.description,
        storyPoints=task.storyPoints,
        priority=task.priority,
        status=task.status
    )