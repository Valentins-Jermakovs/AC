# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Utils
from app.utils.time_converter import convert_to_datetime
# Models
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema
from app.schemas.data.workspace.tasks.workspace_update_task_schema import WorkspaceUpdateTaskSchema


async def update_task(
    data: WorkspaceUpdateTaskSchema,
    user_id: str
) -> WorkspaceTaskSchema:
    
    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": data.projectId,
        "userId": user_id,
    })
    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")

    # ===== Validation =====
    if not ObjectId.is_valid(data.taskId):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    task = await WorkspaceTaskModel.find_one({"_id": ObjectId(data.taskId)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ===== Update fields =====
    if data.title is not None:
        if await WorkspaceTaskModel.find_one({"title": data.title, "_id": {"$ne": task.id}}):
            raise HTTPException(status_code=400, detail="Task title already exists")
        if not (3 <= len(data.title) <= 100):
            raise HTTPException(status_code=400, detail="Title must be between 3 and 100 characters")
        task.title = data.title

    if data.description is not None:
        if not (3 <= len(data.description) <= 1000):
            raise HTTPException(status_code=400, detail="Description must be between 3 and 1000 characters")
        task.description = data.description

    if data.storyPoints is not None:
        if data.storyPoints not in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
            raise HTTPException(status_code=400, detail="Invalid story points")
        task.storyPoints = data.storyPoints

    if data.priority is not None:
        if data.priority not in list(range(1, 11)):
            raise HTTPException(status_code=400, detail="Invalid priority")
        task.priority = data.priority

    if data.status is not None:
        if data.status not in ["todo", "in_progress", "done"]:
            raise HTTPException(status_code=400, detail="Status must be todo, in_progress or done")
        task.status = data.status

    if data.dueDate is not None:
        task.dueDate = await convert_to_datetime(data.dueDate)

    if data.createdAt is not None:
        task.createdAt = await convert_to_datetime(data.createdAt)

    # ===== Save task =====
    await task.save()

    # ===== Return schema =====
    return WorkspaceTaskSchema(
        id=str(task.id),
        projectId=str(task.projectId),
        stageId=str(task.stageId),
        title=task.title,
        description=task.description,
        storyPoints=task.storyPoints,
        priority=task.priority,
        status=task.status,
        createdAt=task.createdAt.strftime("%Y-%m-%d"),
        dueDate=task.dueDate.strftime("%Y-%m-%d") if task.dueDate else None
    )