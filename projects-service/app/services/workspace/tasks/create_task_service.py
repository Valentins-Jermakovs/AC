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
    if not ObjectId.is_valid(task_data.project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Raise if stage_id is not valid
    if not ObjectId.is_valid(task_data.stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # if title not unique
    # Find task with user_id and title
    task = await WorkspaceTaskModel.find_one({
        "projectId": task_data.project_id,
        "stageId": task_data.stage_id,
        "title": task_data.title
    })
    if task:
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    task_order = 0

    # Last task in stage
    last_task = await WorkspaceTaskModel.find_one({
        "stageId": task_data.stage_id
    }).sort("taskOrder", -1)
    if not last_task:
        task_order = 1000.0
    else:
        task_order = last_task.order + 1000.0

    # save new task in DB
    await WorkspaceTaskModel.create({
        "projectId": task_data.project_id,
        "stageId": task_data.stage_id,
        "title": task_data.title,
        "description": task_data.description,
        "storyPoints": task_data.story_points,
        "priority": task_data.priority,
        "status": task_data.status,
        "taskOrder": task_order
    })

    return WorkspaceTaskSchema(
        id=str(ObjectId()),
        projectId=task_data.project_id,
        stageId=task_data.stage_id,
        title=task_data.title,
        description=task_data.description,
        storyPoints=task_data.story_points,
        priority=task_data.priority,
        status=task_data.status
    )