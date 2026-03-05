# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel

# ===============================
# Delete project member
# ===============================
async def delete_project_member(
    projectId: str, 
    userId: str
) -> dict:
    
    # ====== Validation and error handling =====
    # Raise if project_id is not provided
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if user_id is not provided
    if not userId:
        raise HTTPException(status_code=400, detail="User ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # Try to find project member
    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": projectId, "userId": userId
    })
    
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    # Delete project member
    await project_member.delete()

    # Return success message
    return {"message": "Project member deleted successfully"}