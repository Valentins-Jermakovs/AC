# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceProjectMemberModel

from app.services.workspace.selected_project.set_selected_project_service import clear_selected_project_service

# =================================================
# Delete or leave project member
# =================================================
async def delete_project_member(
    project_id: str,
    user_id: str,
    user_id_requester: str
) -> dict:
    """
    Allows a project member to leave the project themselves, or an admin/owner
    to remove another member. Only owner cannot remove themselves.
    """

    # ================= VALIDATION =================
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # ================= FETCH REQUESTER =================
    requester = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id_requester
    })

    if not requester:
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    # ================= SELF LEAVE =================
    if user_id_requester == user_id:
        # Owner cannot leave
        if requester.role == "owner":
            raise HTTPException(
                status_code=403,
                detail="Owner cannot leave the project"
            )

        # Remove self
        await WorkspaceProjectMemberModel.find_one({
            "projectId": project_id,
            "userId": user_id
        }).delete()

        # Clear selected project
        await clear_selected_project_service(user_id)

        return {"message": "You have left the project successfully"}

    # ================= VERIFY PERMISSIONS =================
    # Only admin or owner can remove other members
    if requester.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=403,
            detail="Only admin or owner can remove members"
        )

    # ================= FIND MEMBER TO DELETE =================
    member_to_delete = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if not member_to_delete:
        raise HTTPException(status_code=404, detail="Project member not found")

    # ================= ROLE PROTECTION =================
    # Admin cannot remove owner
    if requester.role == "admin" and member_to_delete.role == "owner":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot remove owner"
        )

    # Admin cannot remove other admin
    if requester.role == "admin" and member_to_delete.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot remove another admin"
        )

    # ================= DELETE =================
    await member_to_delete.delete()

    return {"message": "Project member removed successfully"}