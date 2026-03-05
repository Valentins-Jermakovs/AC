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
    
    # ===== Validation and error handling =====
    # Raise if project_id is not provided
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if user_id is not provided
    if not userId:
        raise HTTPException(status_code=400, detail="User ID is required")
    # Raise if role is not provided
    if not role:
        raise HTTPException(status_code=400, detail="Role is required")
    # Raise if role is not valid
    if role not in ["viewer", "editor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # Try to find project member
    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": projectId, 
        "userId": userId
    })
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    # Update role
    project_member.role = role
    await project_member.save()

    # return project member
    return WorkspaceProjectMemberSchema(
        projectId=project_member.projectId,
        userId=project_member.userId,
        role=project_member.role
    )
