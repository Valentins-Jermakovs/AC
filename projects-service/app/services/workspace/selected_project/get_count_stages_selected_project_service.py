# Imports
from bson import ObjectId
from app.models import WorkspaceStageModel, WorkspaceProjectMemberModel

async def get_stages_count(
    project_id: str,
    user_id: str
) -> int | None:  # <- ļauj None atgriezt
    if not project_id or not ObjectId.is_valid(project_id):
        return None

    # Access check
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        return None

    total_stages = await WorkspaceStageModel.find({
        "projectId": project_id
    }).count()

    return total_stages


async def get_stages_date_range(
    project_id: str,
    user_id: str
) -> dict[str, str] | None:
    if not project_id or not ObjectId.is_valid(project_id):
        return {"startDate": "", "endDate": ""}

    # Access check
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        return {"startDate": "", "endDate": ""}

    total_stages = await WorkspaceStageModel.find({
        "projectId": project_id
    }).count()

    if total_stages == 0:
        return {"startDate": "", "endDate": ""}

    first_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("createdAt").first_or_none()

    last_stage = await WorkspaceStageModel.find({
        "projectId": project_id
    }).sort("-dueDate").first_or_none()

    return {
        "startDate": first_stage.createdAt.strftime("%Y-%m-%d") if first_stage else "",
        "endDate": last_stage.dueDate.strftime("%Y-%m-%d") if last_stage and last_stage.dueDate else ""
    }