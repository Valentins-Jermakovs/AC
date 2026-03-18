# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema

# ==========================================
# Get current user
# Parameters:
# - user_id: The ID of the user
# - project_id: The ID of the board
# Returns:
# - The current user
# ==========================================
async def get_current_user(
    project_id: str,
    user_id: str
) -> WorkspaceProjectMemberSchema:

    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    return WorkspaceProjectMemberSchema(
        email=project_member.email,
        role=project_member.role,
        projectId=project_member.projectId,
        userId=project_member.userId
    )