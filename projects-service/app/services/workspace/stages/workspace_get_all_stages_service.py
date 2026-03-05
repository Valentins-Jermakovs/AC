# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceStageModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema
from app.schemas.response.workspaces.stages.workspace_stage_get_all_schema import WorkspaceGetAllStagesSchema

# =========================
# Get all workspace stages
# =========================
async def get_all_stages(
    project_id: str
) -> WorkspaceGetAllStagesSchema:
    
    # ===== Validation and error handling =====
    # Raise if project_id is not provided
    if not project_id:
        raise HTTPException(status_code=400, detail="Workspace ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid workspace ID")

    # ===== Business logic =====
    # Get all stages
    stages = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("order").to_list()

    # Build response
    items = [WorkspaceStageSchema(
        id=str(stage.id),
        title=stage.title,
        description=stage.description,
        project_id=stage.projectId,
        order=stage.order
    ) for stage in stages]

    # Return response
    return WorkspaceGetAllStagesSchema(
        items=items
    )