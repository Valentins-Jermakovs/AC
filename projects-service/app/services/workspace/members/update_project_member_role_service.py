# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceProjectMemberModel

# Schemas
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema


# =================================================
# Update project member role
# =================================================
async def update_project_member_role(
    project_id: str,
    user_id: str,
    user_id_creator: str,
    role: str
) -> WorkspaceProjectMemberSchema:

    # ================= VALIDATION =================

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_id = ObjectId(project_id)

    role = role.lower().strip()

    if role not in ["viewer", "editor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Block owner assignment
    if role == "owner":
        raise HTTPException(status_code=400, detail="Cannot assign owner role")

    # Block self modification
    if user_id == user_id_creator:
        raise HTTPException(status_code=400, detail="You cannot update yourself")

    # ================= VERIFY CREATOR =================

    creator = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id_creator
    })

    if not creator:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    if creator.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only owner or admin can update roles"
        )

    # ================= FIND MEMBER TO UPDATE =================

    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if not project_member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    # ================= ROLE RESTRICTIONS =================

    # Admin can only assign viewer/editor
    if creator.role == "admin" and role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot assign admin role"
        )

    # Admin cannot modify owner
    if creator.role == "admin" and project_member.role == "owner":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot modify owner"
        )

    # ================= UPDATE =================

    project_member.role = role
    await project_member.save()

    return WorkspaceProjectMemberSchema(
        projectId=project_member.projectId,
        userId=project_member.userId,
        role=project_member.role
    )