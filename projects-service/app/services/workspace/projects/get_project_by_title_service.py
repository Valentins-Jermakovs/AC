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

    query_conditions = []

    if title:
        query_conditions.append(
            {"title": {"$regex": re.escape(title), "$options": "i"}}
        )

    if description:
        query_conditions.append(
            {"description": {"$regex": re.escape(description), "$options": "i"}}
        )

    query = {"$or": query_conditions}

    total_projects = await WorkspaceProjectModel.find(query).count()
    projects = await WorkspaceProjectModel.find(query).skip(offset).limit(limit).to_list()

    total_pages = (total_projects + limit - 1) // limit

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    meta=PaginationMetaSchema(
        page=page,
        limit=limit,
        total_pages=total_pages,
        total_items=total_projects
    )

    items = [
        WorkspaceProjectSchema(
            id=str(project.id),
            title=project.title,
            description=project.description,
            userId=project.userId,
            createdAt=project.createdAt
        ) for project in projects
    ]

    return WorkspaceProjectsPaginatedSchema(items=items, meta=meta)