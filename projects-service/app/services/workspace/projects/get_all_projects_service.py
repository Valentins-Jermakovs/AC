# Imports
from fastapi import HTTPException
# Models
from app.models import WorkspaceProjectModel
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
from app.schemas.response.workspaces.projects.worskpace_projects_paginated_schema import WorkspaceProjectsPaginatedSchema, PaginationMetaSchema

async def get_all_projects(
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> WorkspaceProjectsPaginatedSchema:
    
    # ===== Validation and error handling =====
    # Raise if limit or page not provided
    if not limit or not page:
        raise HTTPException(status_code=400, detail="Limit and page are required")
    # Raise if limit is not a positive integer
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    # Raise if page is not a positive integer
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    # Raise if limit is greater than 100
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    # Raise if user id not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # ===== Business logic =====
    # Pagination offset
    offset = (page - 1) * limit

    query = {}  # Query for database

    if user_id:
        query['userId'] = user_id

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Count total projects
    total_projects = await WorkspaceProjectModel.find(query).count()

    # Get projects
    projects = await WorkspaceProjectModel.find(query).skip(offset).limit(limit).to_list()

    # Get all projects from the database
    items = [
        WorkspaceProjectSchema(
            id=str(project.id),
            userId=project.userId,
            title=project.title,
            description=project.description,
            createdAt=project.createdAt,
        )
        for project in projects
    ]

    # Calculate total pages
    total_pages = (total_projects + limit - 1) // limit

    # Raise if page exceeds total pages
    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")
    # Return projects
    return {
        "items": items,
        "meta": PaginationMetaSchema(
            page=page,
            limit=limit,
            totalItems=total_projects,
            totalPages=total_pages
        )
    }