# Imports
from fastapi import HTTPException
import re
from typing import Optional
# Models
from app.models import WorkspaceProjectModel
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
from app.schemas.response.workspaces.projects.worskpace_projects_paginated_schema import WorkspaceProjectsPaginatedSchema, PaginationMetaSchema

# ===============================
# Function get project by title or description
# ===============================
async def get_project_by_title_or_description(
    title: Optional[str] = None,
    description: Optional[str] = None,
    limit: int = 10,
    page: int = 1
) -> WorkspaceProjectsPaginatedSchema:
    
    if not title and not description:
        raise HTTPException(status_code=400, detail="Title or description required")
    
    if not limit or not page:
        raise HTTPException(status_code=400, detail="Limit and page are required")
    
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    

    # Pagination offset
    offset = (page - 1) * limit

    # Count total projects - filter by title and description in lowercase
    total_projects = await WorkspaceProjectModel.find({
        "$or": [
            {"title": {"$regex": re.escape(title), "$options": "i"}},
            {"description": {"$regex": re.escape(description), "$options": "i"}}
        ]
    }).count()

    # Find projects
    projects = await WorkspaceProjectModel.find({
        "$or": [
            {"title": {"$regex": re.escape(title), "$options": "i"}},
            {"description": {"$regex": re.escape(description), "$options": "i"}}
        ]
    })

    # Return projects
    return WorkspaceProjectsPaginatedSchema(
        data=[WorkspaceProjectSchema(
            id=str(project.id),
            userId=project.userId,
            title=project.title,
            description=project.description,
            createdAt=project.createdAt,
        ) for project in projects],
        meta=PaginationMetaSchema(
            total=total_projects,
            page=page,
            limit=limit
        )
    )