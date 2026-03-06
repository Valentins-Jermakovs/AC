# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceProjectMemberModel


# =================================================
# Delete project member
# =================================================
async def delete_project_member(
    project_id: str,
    user_id: str,
    user_id_creator: str
) -> dict:

    # ================= VALIDATION =================

    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # ================= VERIFY CREATOR =================

    creator = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id_creator
    })

    if not creator:
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    if creator.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=403,
            detail="Only admin or owner can remove members"
        )

    # ================= BLOCK SELF REMOVAL =================

    if user_id_creator == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove yourself"
        )

    # ================= FIND MEMBER TO DELETE =================

    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if not project_member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    # ================= ROLE PROTECTION =================

    # Admin cannot remove owner
    if creator.role == "admin" and project_member.role == "owner":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot remove owner"
        )

    # ================= DELETE =================

    await project_member.delete()

    return {"message": "Project member removed successfully"}