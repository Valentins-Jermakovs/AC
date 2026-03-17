# Imports
from fastapi import HTTPException
import re
from typing import Optional
from bson import ObjectId
# Models
from app.models import WorkspaceProjectModel, WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
from app.schemas.response.workspaces.projects.worskpace_projects_paginated_schema import WorkspaceProjectsPaginatedSchema, PaginationMetaSchema

# ===============================
# Function get project by title or description
# ===============================
async def get_project_by_title(
    user_id: str,
    title: str,
    limit: int = 10,
    page: int = 1
) -> WorkspaceProjectsPaginatedSchema:

    # ================= VALIDATION =================

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not title:
        raise HTTPException(status_code=400, detail="Title required")

    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be positive")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be positive")

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be <= 100")

    offset = (page - 1) * limit

    # ================= CHECK USER EXISTS =================

    user_memberships = await WorkspaceProjectMemberModel.find({
        "userId": user_id
    }).to_list()

    if not user_memberships:
        raise HTTPException(
            status_code=403,
            detail="User is not member of any project"
        )

    # Get project ids where user is member
    project_ids = [ObjectId(member.projectId) for member in user_memberships]

    # ================= BUILD SEARCH QUERY =================

    query_conditions = []

    if title:
        query_conditions.append({
            "title": {
                "$regex": re.escape(title),
                "$options": "i"
            }
        })

    if not query_conditions:
        raise HTTPException(status_code=400, detail="Invalid search parameters")

    # Search ONLY inside user's projects
    query = {
        "_id": {"$in": project_ids},
        "$or": query_conditions
    }

    # ================= COUNT =================

    total_projects = await WorkspaceProjectModel.find(query).count()

    if total_projects == 0:
        raise HTTPException(status_code=404, detail="No projects found")

    total_pages = (total_projects + limit - 1) // limit

    if offset >= total_projects:
        raise HTTPException(status_code=404, detail="Page not found")

    # ================= FETCH =================
    projects = await WorkspaceProjectModel.find(query).skip(offset).limit(limit).to_list()

    # ================= RESPONSE =================

    items = [
        WorkspaceProjectSchema(
            id=str(project.id),
            title=project.title,
            description=project.description,
            userId=project.userId,
            createdAt=project.createdAt
        )
        for project in projects
    ]

    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=total_pages,
        totalItems=total_projects
    )

    return WorkspaceProjectsPaginatedSchema(
        items=items,
        meta=meta
    )