# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceStageModel, WorkspaceTaskModel, WorkspaceProjectMemberModel

# =========================
# Delete a workspace stage
# =========================
async def delete_stage(
    stage_id: str,
    project_id: str,
    user_id: str
) -> dict:

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

    # Delete tasks
    await WorkspaceTaskModel.find({
        "stageId": stage_id
    }).delete()

    # Delete stage
    await stage.delete()

    return {"message": f"Stage '{stage.title}' deleted successfully"}