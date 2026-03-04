# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel
# Schemas
from app.schemas.response.workspaces.tasks.workspace_task_list_schema import WorkspaceTaskListSchema
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema

async def get_all_tasks(
    projectId: str,
    stageId: str
) -> WorkspaceTaskListSchema:

    # Raise if project_id is not valid
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")

    # Raise if stage_id is not valid
    if not stageId:
        raise HTTPException(status_code=400, detail="Stage ID is required")

    # Raise if project_id is not valid
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Raise if stage_id is not valid
    if not ObjectId.is_valid(stageId):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    tasks = await WorkspaceTaskModel.find({
        "projectId": projectId,
        "stageId": stageId
    }).sort("order").to_list()

    items = [
        WorkspaceTaskSchema(
            id=str(task.id),
            projectId=task.projectId,
            stageId=task.stageId,
            title=task.title,
            description=task.description,
            storyPoints=task.storyPoints,
            priority=task.priority,
            status=task.status
        ) for task in tasks
    ]

    return WorkspaceTaskListSchema(items=items)