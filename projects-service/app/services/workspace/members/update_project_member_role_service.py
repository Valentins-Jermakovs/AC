# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema

# ===============================
# Update project member role
# ===============================
async def update_project_member_role(
    projectId: str, 
    userId: str, 
    role: str
) -> WorkspaceProjectMemberSchema:
    
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not userId:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not role:
        raise HTTPException(status_code=400, detail="Role is required")

    if role not in ["viewer", "editor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": projectId, 
        "userId": userId
    })
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    project_member.role = role
    await project_member.save()

    return WorkspaceProjectMemberSchema(
        project_id=project_member.projectId,
        user_id=project_member.userId,
        role=project_member.role
    )
