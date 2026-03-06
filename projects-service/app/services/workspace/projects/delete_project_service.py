# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import (
    WorkspaceProjectModel,
    WorkspaceStageModel,
    WorkspaceProjectMemberModel,
    WorkspaceTaskModel
)

async def delete_project(project_id: str, user_id: str) -> dict:

    # Check if current user is owner of this project
    if not await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
        "role": "owner"
    }):
        raise HTTPException(status_code=403, detail="You are not owner of this project or this project does not exist")
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Try to find project
    project = await WorkspaceProjectModel.find_one({"_id": ObjectId(project_id)})

    # Raise if project not found
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    
    # Delete all stages
    await WorkspaceStageModel.find({
        "projectId": project_id
    }).delete()

    # Delete all project members
    await WorkspaceProjectMemberModel.find({
        "projectId": project_id
    }).delete()

    # Delete all tasks
    await WorkspaceTaskModel.find({
        "projectId": project_id
    }).delete()

    # Delete project
    await project.delete()

    return {"message": f"Project '{project.title}' deleted successfully"}