# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
from app.schemas.response.workspaces.projects.worskpace_projects_paginated_schema import WorkspaceProjectsPaginatedSchema, PaginationMetaSchema

async def get_all_projects(
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> WorkspaceProjectsPaginatedSchema:

    # ===== Validation and error handling =====
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be positive")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be positive")

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be <= 100")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID required")


    # ===== Business logic =====
    offset = (page - 1) * limit

    members = await WorkspaceProjectMemberModel.find({
        "userId": user_id
    }).to_list()

    total_projects = len(members)

    if total_projects == 0:
        raise HTTPException(status_code=404, detail="No projects found")

    if offset >= total_projects:
        raise HTTPException(status_code=404, detail="Page not found")

    project_ids = [ObjectId(member.projectId) for member in members]

    projects = await WorkspaceProjectModel.find({
        "_id": {"$in": project_ids}
    }).skip(offset).limit(limit).to_list()

    items = [
        WorkspaceProjectSchema(
            id=str(project.id),
            userId=project.userId,
            title=project.title,
            description=project.description,
            createdAt=project.createdAt
        )
        for project in projects
    ]

    total_pages = (total_projects + limit - 1) // limit

    return WorkspaceProjectsPaginatedSchema(
        items=items,
        meta=PaginationMetaSchema(
            page=page,
            limit=limit,
            totalItems=total_projects,
            totalPages=total_pages
        )
    )

# =========================
# Get projects count
# =========================
async def get_projects_count(user_id: str) -> int:

    # ===== Validation =====
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID required")

    # ===== Business logic =====
    total_projects = await WorkspaceProjectMemberModel.find({
        "userId": user_id
    }).count()

    return total_projects