from fastapi import HTTPException
from ...models import WorkspaceProjectModel
from typing import Optional
from bson import ObjectId
from ...schemas.response.workspace_project import WorkspaceProjectSchema

async def update_project (
    project_id: str,
    title: str,
    description: Optional[str] = None
):
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Get project
    project = await WorkspaceProjectModel.find_one({"_id": ObjectId(project_id)})

    # Raise if project not found
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Raise if title is empty
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # Raise if desciption or title are the same
    if title == project.title and description == project.description:
        raise HTTPException(status_code=400, detail="Title and description are the same")

    # If description not exist
    if description is None:
        description = ""

    # Update project
    await project.set({"title": title, "description": description})

    return WorkspaceProjectSchema(
        id=str(project.id),              # ObjectId -> str
        userId=project.userId,
        title=project.title,
        description=project.description,
        createdAt=project.createdAt
    )