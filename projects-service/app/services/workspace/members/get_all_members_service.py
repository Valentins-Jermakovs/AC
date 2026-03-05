# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema

# ===============================
# Get all project members
# ===============================
async def get_all_project_members(
    projectId: str
) -> dict:
    
    # Raise if project_id is not valid
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # Get all project members
    members = await WorkspaceProjectMemberModel.find(
        WorkspaceProjectMemberModel.projectId == projectId
    ).to_list()

    # Raise if members not found
    if not members:
        raise HTTPException(status_code=404, detail="Members not found")

    return {
        "members": [
            WorkspaceProjectMemberSchema(
                projectId=member.projectId,
                userId=member.userId,
                role=member.role
            )
            for member in members
        ]
    }