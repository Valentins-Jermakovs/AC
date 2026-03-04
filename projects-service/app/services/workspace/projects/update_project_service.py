# Imports
from fastapi import HTTPException
from app.models import WorkspaceProjectModel
from typing import Optional
from bson import ObjectId
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
# Models
from app.models import WorkspaceProjectModel

async def update_project (
    project_id: str,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> WorkspaceProjectSchema:
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Get project
    project = await WorkspaceProjectModel.find_one({"_id": ObjectId(project_id)})

    # Raise if project not found
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Raise if title is empty
    if not title and not description:
        raise HTTPException(status_code=400, detail="No data to update")
    
    # Title uniqness check
    if await WorkspaceProjectModel.find_one({
        "title": title,
        "userId": user_id,
        "_id": {"$ne": project.id}
    }):
        raise HTTPException(status_code=400, detail="Title must be unique")

    # Decription check
    if description is not None:
        description = description.strip()
        # Raise if description is too long
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
        # Raise if desrciption or title are the same
        if description == project.description:
            raise HTTPException(status_code=400, detail="Description is the same")

    update_data = {}

    if title is not None:
        update_data["title"] = title

    if description is not None:
        update_data["description"] = description

    await project.set(update_data)

    return WorkspaceProjectSchema(
        id=str(project.id),              # ObjectId -> str
        userId=project.userId,
        title=project.title,
        description=project.description,
        createdAt=project.createdAt
    )