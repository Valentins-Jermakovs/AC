# Imports
from typing import Optional
from fastapi import HTTPException
# Models
from app.models import WorkspaceProjectModel
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema

# Secondary services
from app.services.workspace.members.add_project_member_service import add_project_member

# ================================
# Function create project
# =================================
async def create_project(
    email: str,
    title: str,
    user_id: str,
    description: Optional[str] = None
) -> WorkspaceProjectSchema:
    
    # ===== Validation and error handling =====
    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    # Raise if title is empty
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    title = title.strip()

    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    # Check title uniuqe
    if await WorkspaceProjectModel.find_one({"title": title}):
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    if description is not None:
        # Raise if description is too long
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")

    # ===== Business logic =====
    # Create new project
    new_project = WorkspaceProjectModel(
        userId=user_id,
        title=title,
        description=description
    )

    # Save new document in MongoDb
    await new_project.save()

    # Add owner of board to members collection
    await add_project_member(
        project_id=str(new_project.id),
        email=email,
        user_id=user_id,
        user_id_creator=user_id,
        role="owner",
        mode="create_owner"
    )

    # ===== Response =====
    return WorkspaceProjectSchema(
        id=str(new_project.id),              # ObjectId -> str
        userId=new_project.userId,
        title=new_project.title,
        description=new_project.description,
        createdAt=new_project.createdAt
    )
