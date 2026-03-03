# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel

# ================================
# Add project member
# ================================
async def add_project_member(
    projectId: str, 
    userId: str, 
    role: str
) -> dict:
    
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
    
    project_member = WorkspaceProjectMemberModel(
        projectId=projectId,
        userId=userId,
        role=role
    )

    await project_member.save()

    return {"message": "Project member added successfully"}