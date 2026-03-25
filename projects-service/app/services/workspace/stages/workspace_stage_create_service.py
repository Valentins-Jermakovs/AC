# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
from datetime import datetime

# Models
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel

# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema

# Utils
from app.utils.time_converter import convert_to_datetime
from app.utils.current_date import get_current_date  # auto datetime

# =========================
# Create a new workspace stage
# =========================
async def create_stage(
    title: str,
    project_id: str,
    user_id: str,
    created_at: Optional[str] = None,
    due_date: Optional[str] = None,
    description: Optional[str] = None,
) -> WorkspaceStageSchema:
    
    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")
    
    # ===== Validation =====
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    if description is not None:
        if not description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
    
    # ===== Dates handling =====
    if created_at:
        created_at_dt = await convert_to_datetime(created_at)
    else:
        created_at_dt = get_current_date()  # if created_at is None

    if due_date:
        str_due = due_date.strip()
        due_date_dt = await convert_to_datetime(due_date)
    else:
        str_due = None
        due_date_dt = None

    # Check title unique per project
    if await WorkspaceStageModel.find_one({"title": title, "projectId": project_id}):
        raise HTTPException(status_code=400, detail="Title must be unique in this project")
    
    # ===== Business logic =====
    # Last stage in board
    last_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("-order").first_or_none()

    order = last_stage.order + 1000.0 if last_stage else 1000.0
    
    # Create new stage
    new_stage = WorkspaceStageModel(
        title=title,
        description=description,
        projectId=project_id,
        order=order,
        createdAt=created_at_dt,
        dueDate=due_date_dt,
    )
    
    await new_stage.insert()
    
    return WorkspaceStageSchema(
        id=str(new_stage.id),
        title=new_stage.title,
        description=new_stage.description,
        projectId=new_stage.projectId,
        order=new_stage.order,
        dueDate=str_due,
        createdAt=new_stage.createdAt.strftime("%Y-%m-%d")
    )