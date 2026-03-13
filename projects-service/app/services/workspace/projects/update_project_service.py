# Imports
from fastapi import HTTPException
from typing import Optional
from bson import ObjectId
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
# Models
from app.models import WorkspaceProjectModel, WorkspaceProjectMemberModel

async def update_project (
    project_id: str,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> WorkspaceProjectSchema:
    
    # Check if current user is owner of this project
    if not await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
        "role": "owner"
    }):
        raise HTTPException(status_code=403, detail="You are not owner of this project or this project does not exist")


    # ===== Validation and error handling =====
    # Raise if project_id is not provided
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    # Raise if not user_id
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # ===== Business logic =====
    # Get project
    project = await WorkspaceProjectModel.find_one({"_id": ObjectId(project_id)})
    # Raise if project not found
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Raise if title and data is empty
    if not title and not description:
        raise HTTPException(status_code=400, detail="No data to update")
    
    # Title uniqness check
    if await WorkspaceProjectModel.find_one({
        "title": title,
        "userId": user_id,
        "_id": {"$ne": project.id}
    }):
        raise HTTPException(status_code=400, detail="Title must be unique")

    # ===== Validation and error handling =====
    # Description check
    if description is not None:
        description = description.strip()
        # Raise if description is too long
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")

    # ===== Business logic =====
    update_data = {}

    # Update data
    if title is not None:
        update_data["title"] = title

    if description is not None:
        update_data["description"] = description

    # Update project
    await project.set(update_data)

    # Return project
    return WorkspaceProjectSchema(
        id=str(project.id),              # ObjectId -> str
        userId=project.userId,
        title=project.title,
        description=project.description,
        createdAt=project.createdAt
    )