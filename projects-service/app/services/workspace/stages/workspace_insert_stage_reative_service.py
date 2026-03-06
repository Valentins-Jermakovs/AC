# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema


async def insert_stage_relative(
    project_id: str,
    title: str,
    user_id: str,
    reference_stage_id: str, # stage which will be used as reference
    position: str,  # "before" or "after"
    description: Optional[str] = None,
    
) -> WorkspaceStageSchema:
    
    # ===== Validation and error handling =====
    # Raise if project_id is not provided
    if project_id is None:
        raise HTTPException(status_code=400, detail="Board ID is required")
    # Raise if project_id is not valid
    if title is None:
        raise HTTPException(status_code=400, detail="Title is required")
    # Raise if title is empty
    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    # Raise if reference_stage_id is not provided
    if reference_stage_id is None:
        raise HTTPException(status_code=400, detail="Reference stage ID is required")
    # Raise if reference_stage_id is not valid
    if not ObjectId.is_valid(reference_stage_id):
        raise HTTPException(status_code=400, detail="Invalid reference stage ID")
    # Raise if position is not valid
    if position not in ["before", "after"]:
        raise HTTPException(status_code=400, detail="Position must be 'before' or 'after'")


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

    # if title not unique
    # Find stage with user_id and title
    stage = await WorkspaceStageModel.find_one({
        "title": title,
        "projectId": project_id
    })
    if stage:
        raise HTTPException(status_code=400, detail="Title must be unique")

    # Find reference stage
    reference_stage = await WorkspaceStageModel.find_one({
        "projectId": project_id,
        "_id": ObjectId(reference_stage_id)
    })

    # Raise if stage not found
    if not reference_stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Find neighbour depending on position
    if position == "after":

        # Find next stage
        next_stage = await WorkspaceStageModel.find({
            "projectId": project_id,
            "order": {"$gt": reference_stage.order}
        }).sort("order").first_or_none()

        # Calculate new order
        if next_stage:
            new_order = (next_stage.order + reference_stage.order) / 2
        else:
            new_order = reference_stage.order + 1000.0
    
    elif position == "before":
        prev_stage = await WorkspaceStageModel.find({
            "projectId": project_id,
            "order": {"$lt": reference_stage.order}
        }).sort("-order").first_or_none()

        # Calculate new order
        if prev_stage:
            new_order = (prev_stage.order + reference_stage.order) / 2
        else:
            new_order = reference_stage.order - 1000.0

    else:
        raise HTTPException(status_code=400, detail="Invalid position")

    # Create new stage
    stage = WorkspaceStageModel(
        projectId=project_id,
        title=title,
        order=new_order
    )

    # Add description
    if description is not None:
        stage.description = description

    # Insert stage
    await stage.insert()

    # Return stage
    return WorkspaceStageSchema(
        id=str(stage.id),
        projectId=stage.projectId,
        title=stage.title,
        order=stage.order,
        description=stage.description,
        createdAt=stage.createdAt
    )