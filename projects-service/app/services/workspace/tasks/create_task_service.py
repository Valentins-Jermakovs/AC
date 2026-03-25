# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Utils
from app.utils.time_converter import convert_to_datetime
from app.utils.current_date import get_current_date
# Models
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema
from app.schemas.data.workspace.tasks.workspace_create_task_schema import WorkspaceCreateTaskSchema


async def create_task(
    task_data: WorkspaceCreateTaskSchema,
    user_id: str
) -> WorkspaceTaskSchema:
    
    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": task_data.projectId,
        "userId": user_id,
    })
    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")
    
    # ===== Validation =====
    if not ObjectId.is_valid(task_data.projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    if not ObjectId.is_valid(task_data.stageId):
        raise HTTPException(status_code=400, detail="Invalid stage ID")
    
    if await WorkspaceTaskModel.find_one({
        "projectId": task_data.projectId,
        "stageId": task_data.stageId,
        "title": task_data.title
    }):
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    if not (3 <= len(task_data.title) <= 100):
        raise HTTPException(status_code=400, detail="Title must be between 3 and 100 characters")
    
    if task_data.status not in ["todo", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    if task_data.priority not in list(range(1, 11)):
        raise HTTPException(status_code=400, detail="Invalid priority")
    
    if task_data.storyPoints not in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
        raise HTTPException(status_code=400, detail="Invalid story points")
    
    if task_data.description:
        if not task_data.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        if len(task_data.description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
    
    # ===== Convert dates =====
    if task_data.dueDate:
        due_date_dt = await convert_to_datetime(task_data.dueDate)
    else:
        due_date_dt = None
    
    if task_data.createdAt:
        created_at_dt = await convert_to_datetime(task_data.createdAt)
    else:
        created_at_dt = get_current_date()

    # ===== Calculate task order =====
    last_task = await WorkspaceTaskModel.find({
        "stageId": task_data.stageId
    }).sort("-order").first_or_none()

    task_order = last_task.order + 1000.0 if last_task else 1000.0

    # ===== Create new task =====
    new_task = WorkspaceTaskModel(
        projectId=task_data.projectId,
        stageId=task_data.stageId,
        title=task_data.title,
        description=task_data.description,
        storyPoints=task_data.storyPoints,
        priority=task_data.priority,
        status=task_data.status,
        order=task_order,
        createdAt=created_at_dt,
        dueDate=due_date_dt
    )

    await new_task.insert()

    # ===== Return schema =====
    return WorkspaceTaskSchema(
        id=str(new_task.id),
        projectId=task_data.projectId,
        stageId=task_data.stageId,
        title=task_data.title,
        description=task_data.description,
        storyPoints=task_data.storyPoints,
        priority=task_data.priority,
        status=task_data.status,
        createdAt=new_task.createdAt.strftime("%Y-%m-%d"),
        dueDate=due_date_dt.strftime("%Y-%m-%d") if due_date_dt else None
    )