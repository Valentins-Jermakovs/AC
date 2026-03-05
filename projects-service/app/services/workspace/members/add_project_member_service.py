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
    
    # check existing users
    if await WorkspaceProjectMemberModel.find_one({
        "projectId": projectId, 
        "userId": userId
    }):
        raise HTTPException(status_code=400, detail="Project member already exists")

    # Add project member
    project_member = WorkspaceProjectMemberModel(
        projectId=projectId,
        userId=userId,
        role=role
    )

    # Save project member
    await project_member.save()

    # Return success message
    return {"message": "Project member added successfully"}