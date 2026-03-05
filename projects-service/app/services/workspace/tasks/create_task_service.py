# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel
# Schemas
# ===== response:
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema
# ===== data:
from app.schemas.data.workspace.tasks.workspace_create_task_schema import WorkspaceCreateTaskSchema

# ===============================
# Function create task
# ================================
async def create_task(
    task_data: WorkspaceCreateTaskSchema
) -> WorkspaceTaskSchema:
    
    # Raise if project_id is not valid
    if not ObjectId.is_valid(task_data.projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Raise if stage_id is not valid
    if not ObjectId.is_valid(task_data.stageId):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # if title not unique
    # Find task with user_id and title
    task = await WorkspaceTaskModel.find_one({
        "projectId": task_data.projectId,
        "stageId": task_data.stageId,
        "title": task_data.title
    })
    if task:
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    if len(task_data.title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(task_data.title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    task_order = 0

    # Last task in stage
    last_task = await WorkspaceTaskModel.find({
        "stageId": task_data.stageId}
    ).sort("-order").first_or_none()

    if not last_task:
        task_order = 1000.0
    else:
        task_order = last_task.order + 1000.0

    if task_data.status not in ["todo", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    if task_data.priority not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        raise HTTPException(status_code=400, detail="Invalid priority")
    
    if task_data.storyPoints not in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
        raise HTTPException(status_code=400, detail="Invalid story points")
    
    if task_data.description is not None:
        if not task_data.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")

        if len(task_data.description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")


    # save new task in DB
    new_task = WorkspaceTaskModel(
        projectId=task_data.projectId,
        stageId=task_data.stageId,
        title=task_data.title,
        description=task_data.description,
        storyPoints=task_data.storyPoints,
        priority=task_data.priority,
        status=task_data.status,
        order=task_order
    )

    # insert new task
    await new_task.insert()

    # return created task
    return WorkspaceTaskSchema(
        id=str(ObjectId()),
        projectId=task_data.projectId,
        stageId=task_data.stageId,
        title=task_data.title,
        description=task_data.description,
        storyPoints=task_data.storyPoints,
        priority=task_data.priority,
        status=task_data.status
    )