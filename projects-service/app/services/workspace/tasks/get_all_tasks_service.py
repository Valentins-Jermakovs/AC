# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.tasks.workspace_task_list_schema import WorkspaceTaskListSchema
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema

async def get_all_tasks(
    project_id: str,
    stage_id: str,
    user_id: str
) -> WorkspaceTaskListSchema:

    # ===== Validation and error handling =====

    # Check current user
    user =  await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")

    # Raise if project_id is not valid
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if stage_id is not valid
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    # Raise if stage_id is not valid
    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # ===== Business logic =====
    # Get all tasks
    tasks = await WorkspaceTaskModel.find({
        "projectId": project_id,
        "stageId": stage_id
    }).sort("order").to_list()

    # Build response
    items = [
        WorkspaceTaskSchema(
            id=str(task.id),
            projectId=task.projectId,
            stageId=task.stageId,
            title=task.title,
            description=task.description,
            storyPoints=task.storyPoints,
            priority=task.priority,
            status=task.status,
            createdAt=task.createdAt.strftime("%Y-%m-%d"),
            dueDate=task.dueDate.strftime("%Y-%m-%d")
        ) for task in tasks
    ]

    # Return response
    return WorkspaceTaskListSchema(
        items=items
    )