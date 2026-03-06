# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceProjectMemberModel

# ==================================================
# Function add project member
# ==================================================
async def add_project_member(
    project_id: str,
    user_id: str,
    user_id_creator: str,
    mode: str,
    role: str,
) -> dict:

    # ================= VALIDATION =================

    if not project_id:
        raise HTTPException(400, "Project ID is required")

    if not user_id:
        raise HTTPException(400, "User ID is required")

    if not role:
        raise HTTPException(400, "Role is required")

    if mode not in ["create_owner", "add"]:
        raise HTTPException(400, "Invalid mode")

    role = role.lower().strip()

    if role not in ["viewer", "editor", "admin", "owner"]:
        raise HTTPException(400, "Invalid role")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(400, "Invalid project ID")

    project_id = ObjectId(project_id)

    # ================= CREATE OWNER MODE =================

    if mode == "create_owner":

        project_member = WorkspaceProjectMemberModel(
            projectId=project_id,
            userId=user_id,
            role="owner"
        )

        await project_member.save()

        return project_member

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

    if creator.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=403,
            detail="You are not admin or owner of this project"
        )

    # ================= BLOCK SELF MODIFICATION =================

    if user_id_creator == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot modify yourself"
        )

    # ================= BLOCK OWNER CREATION =================

    if role == "owner":
        raise HTTPException(
            status_code=403,
            detail="Owner cannot be added"
        )

    # ================= ADMIN RESTRICTIONS =================

    if creator.role == "admin" and role in ["admin", "owner"]:
        raise HTTPException(
            status_code=403,
            detail="Admin cannot assign this role"
        )

    # ================= CHECK EXISTING MEMBER =================

    existing_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Project member already exists"
        )

    # ================= CREATE MEMBER =================

    project_member = WorkspaceProjectMemberModel(
        projectId=project_id,
        userId=user_id,
        role=role
    )

    await project_member.save()

    return {
        "message": "Project member created successfully"
    }