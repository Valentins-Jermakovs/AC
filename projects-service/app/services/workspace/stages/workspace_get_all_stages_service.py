# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema
from app.schemas.response.workspaces.stages.workspace_stage_get_all_schema import WorkspaceGetAllStagesSchema

# =========================
# Get all workspace stages
# =========================
async def get_all_stages(
    project_id: str,
    user_id: str
) -> WorkspaceGetAllStagesSchema:
    
    # ===== Validation and error handling =====
    # Raise if project_id is not provided
    if not project_id:
        raise HTTPException(status_code=400, detail="Workspace ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid workspace ID")

    # ===== Current user handling =====
    # Check role of current user
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this workspace or this workspace does not exist")

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
        projectId=stage.projectId,
        order=stage.order,
        dueDate=stage.dueDate.strftime("%Y-%m-%d"),
        createdAt=stage.createdAt.strftime("%Y-%m-%d")
    ) for stage in stages]

    # Return response
    return WorkspaceGetAllStagesSchema(
        items=items
    )