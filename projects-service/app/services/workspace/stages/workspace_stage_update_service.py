# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from app.models import WorkspaceStageModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema

# =========================
# Update a workspace stage
# =========================
async def update_stage(
    stage_id: str,
    title: str,
    description: Optional[str] = None,
) -> WorkspaceStageSchema:
    
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

        stage.title = title

    if description is not None:

        if not description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")

        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        
        stage.description = description

    await stage.save()

    return WorkspaceStageSchema(
        id=str(stage.id),
        title=stage.title,
        description=stage.description,
        project_id=str(stage.projectId),
        order=stage.order
    )