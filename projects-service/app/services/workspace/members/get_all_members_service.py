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
    
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    members = await WorkspaceProjectMemberModel.find(
        WorkspaceProjectMemberModel.projectId == projectId
    ).to_list()

    if not members:
        raise HTTPException(status_code=404, detail="Members not found")

    return {
        "members": [
            WorkspaceProjectMemberSchema(
                project_id=member.projectId,
                user_id=member.userId,
                role=member.role
            )
            for member in members
        ]
    }