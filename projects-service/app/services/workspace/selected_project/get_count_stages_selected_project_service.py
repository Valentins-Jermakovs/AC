# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel


async def get_stages_count(
    project_id: str,
    user_id: str
) -> int:

    # ===== Validation =====
    if not project_id:
        raise HTTPException(status_code=400, detail="Workspace ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid workspace ID")

    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(
            status_code=403,
            detail="You are not member of this workspace or this workspace does not exist"
        )

    # ===== Business logic =====
    total_stages = await WorkspaceStageModel.find({
        "projectId": project_id
    }).count()

    return total_stages

async def get_stages_date_range(
    project_id: str,
    user_id: str
):

    # ===== Validation =====
    if not project_id:
        raise HTTPException(status_code=400, detail="Workspace ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid workspace ID")

    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(
            status_code=403,
            detail="You are not member of this workspace"
        )

    # ===== Count stages =====
    total_stages = await WorkspaceStageModel.find({
        "projectId": project_id
    }).count()

    # ===== No stages =====
    if total_stages == 0:
        return {
            "startDate": "",
            "endDate": ""
        }

    # ===== First stage (by createdAt) =====
    first_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("createdAt").first_or_none()

    # ===== Last stage (by dueDate) =====
    last_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("-dueDate").first_or_none()

    return {
        "startDate": first_stage.createdAt.strftime("%Y-%m-%d") if first_stage else "",
        "endDate": last_stage.dueDate.strftime("%Y-%m-%d") if last_stage and last_stage.dueDate else ""
    }