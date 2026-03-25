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

async def insert_stage_relative(
    project_id: str,
    title: str,
    user_id: str,
    reference_stage_id: str,  # stage which will be used as reference
    position: str,  # "before" or "after"
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    created_at: Optional[str] = None
) -> WorkspaceStageSchema:
    
    # ===== Validation =====
    if not project_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    if not reference_stage_id:
        raise HTTPException(status_code=400, detail="Reference stage ID is required")
    if not ObjectId.is_valid(reference_stage_id):
        raise HTTPException(status_code=400, detail="Invalid reference stage ID")
    if position not in ["before", "after"]:
        raise HTTPException(status_code=400, detail="Position must be 'before' or 'after'")

    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })
    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this project")
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot work in this project")

    # ===== Check title uniqueness =====
    existing_stage = await WorkspaceStageModel.find_one({
        "title": title,
        "projectId": project_id
    })
    if existing_stage:
        raise HTTPException(status_code=400, detail="Title must be unique in this project")

    # ===== Find reference stage =====
    reference_stage = await WorkspaceStageModel.find_one({
        "projectId": project_id,
        "_id": ObjectId(reference_stage_id)
    })
    if not reference_stage:
        raise HTTPException(status_code=404, detail="Reference stage not found")

    # ===== Calculate order =====
    if position == "after":
        next_stage = await WorkspaceStageModel.find({
            "projectId": project_id,
            "order": {"$gt": reference_stage.order}
        }).sort("order").first_or_none()
        new_order = (next_stage.order + reference_stage.order) / 2 if next_stage else reference_stage.order + 1000.0

    elif position == "before":
        prev_stage = await WorkspaceStageModel.find({
            "projectId": project_id,
            "order": {"$lt": reference_stage.order}
        }).sort("-order").first_or_none()
        new_order = (prev_stage.order + reference_stage.order) / 2 if prev_stage else reference_stage.order - 1000.0

    # ===== Handle dates =====
    if created_at:
        created_at_dt = await convert_to_datetime(created_at)
    else:
        created_at_dt = get_current_date()

    if due_date:
        str_due = due_date.strip()
        due_date_dt = await convert_to_datetime(due_date)
    else:
        str_due = None
        due_date_dt = None

    # ===== Create new stage =====
    stage = WorkspaceStageModel(
        projectId=project_id,
        title=title,
        order=new_order,
        createdAt=created_at_dt,
        dueDate=due_date_dt,
        description=description
    )

    await stage.insert()

    # ===== Return schema =====
    return WorkspaceStageSchema(
        id=str(stage.id),
        projectId=stage.projectId,
        title=stage.title,
        order=stage.order,
        description=stage.description,
        createdAt=stage.createdAt.strftime("%Y-%m-%d"),
        dueDate=str_due
    )