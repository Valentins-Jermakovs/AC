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
# Create a new workspace stage
# =========================
async def create_stage(
    title: str,
    project_id: str,
    user_id: str,
    due_date: Optional[str] = None,
    description: Optional[str] = None,
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
    
    # ===== Validation and error handling =====
    # Raise if title is empty
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    # Raise if project_id is not provided
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
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
    
    if due_date is not None:
        str_date = due_date.strip()
        due_date = await convert_to_datetime(due_date)

    # Check title uniuqe
    if await WorkspaceStageModel.find_one({"title": title}):
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    # ===== Business logic =====
    # Last stage in board
    last_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("-order").first_or_none()

    # if stages not exist
    if not last_stage:
        order = 1000.0
    else:
        order = last_stage.order + 1000.0
    
    # Create new stage
    new_stage = WorkspaceStageModel(
        title=title,
        description=description,
        projectId=project_id,
        order=order,
        dueDate=due_date
    )
    
    await new_stage.insert()
    
    return WorkspaceStageSchema(
        id=str(new_stage.id),
        title=new_stage.title,
        description=new_stage.description,
        projectId=new_stage.projectId,
        order=new_stage.order,
        dueDate=str_date
    )
