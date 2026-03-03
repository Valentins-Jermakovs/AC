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
    
    if not projectId:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not userId:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_member = await WorkspaceProjectMemberModel.find_one({
        "projectId": projectId, "userId": userId
    })
    
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    await project_member.delete()

    return {"message": "Project member deleted successfully"}