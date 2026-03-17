# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema
# Utils
from app.utils.time_converter import convert_to_datetime

# =========================
# Update a workspace stage
# =========================
async def update_stage(
    stage_id: str,
    title: str,
    user_id: str,
    project_id: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None
) -> WorkspaceStageSchema:
    
    # Check current user
    user =  await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    
    # Check if user is viewer
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")
    
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # Find stage
    stage = await WorkspaceStageModel.find_one({
        "_id": ObjectId(stage_id)
    })

    # Raise if stage not found
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    if title is not None:

        # check title uniqness
        if await WorkspaceStageModel.find_one({
            "title": title,
            "projectId": stage.projectId,
            "_id": {"$ne": stage.id}
        }):
            raise HTTPException(status_code=400, detail="Title must be unique")

        # Raise if title is empty
        if not title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        # Raise if title is too long
        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        # Raise if title is too short
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")

        # Update title
        stage.title = title

    if description is not None:

        # Raise if description is empty
        if not description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        # Raise if description is too long
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        
        # Update description
        stage.description = description

    if due_date is not None:
        # Convert due date to datetime
        due_date = await convert_to_datetime(due_date)

        # Update due date
        stage.dueDate = due_date

    # Update stage
    await stage.save()

    return WorkspaceStageSchema(
        id=str(stage.id),
        title=stage.title,
        description=stage.description,
        projectId=str(stage.projectId),
        order=stage.order,
        dueDate=stage.dueDate.strftime("%Y-%m-%d")
    )