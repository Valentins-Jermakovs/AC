# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceStageModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema

# =========================
# Create a new workspace stage
# =========================
async def create_stage(
    title: str,
    description: str,
    project_id: str,
) -> WorkspaceStageSchema:
    # Raise if title is empty
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
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
    
    # Check title uniuqe
    if await WorkspaceStageModel.find_one({"title": title}):
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
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
        order=order
    )
    
    await new_stage.insert()
    
    return WorkspaceStageSchema(
        id=str(new_stage.id),
        title=new_stage.title,
        description=new_stage.description,
        project_id=new_stage.projectId,
        order=new_stage.order
    )
