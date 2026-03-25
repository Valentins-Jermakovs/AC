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
# Update a workspace stage
# =========================
async def update_stage(
    stage_id: str,
    title: Optional[str],
    user_id: str,
    project_id: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    created_at: Optional[str] = None,
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
    
    # ===== Stage validation =====
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    stage = await WorkspaceStageModel.find_one({"_id": ObjectId(stage_id)})
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # ===== Update title =====
    if title is not None:
        if await WorkspaceStageModel.find_one({
            "title": title,
            "projectId": stage.projectId,
            "_id": {"$ne": stage.id}
        }):
            raise HTTPException(status_code=400, detail="Title must be unique in this project")
        if not title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")
        stage.title = title

    # ===== Update description =====
    if description is not None:
        if not description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        stage.description = description

    # ===== Update due date =====
    if due_date is not None:
        stage.dueDate = await convert_to_datetime(due_date)

    # ===== Update created_at =====
    if created_at is not None:
        stage.createdAt = await convert_to_datetime(created_at)

    # ===== Save changes =====
    await stage.save()

    # ===== Return schema =====
    return WorkspaceStageSchema(
        id=str(stage.id),
        title=stage.title,
        description=stage.description,
        projectId=str(stage.projectId),
        order=stage.order,
        dueDate=stage.dueDate.strftime("%Y-%m-%d") if stage.dueDate else None,
        createdAt=stage.createdAt.strftime("%Y-%m-%d") if stage.createdAt else None
    )