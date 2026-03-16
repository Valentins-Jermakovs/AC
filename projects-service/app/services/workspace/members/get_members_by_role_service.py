# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceProjectMemberModel
# Schemas
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema
from app.schemas.response.workspaces.members.workspace_members_paginated import (
    WorkspaceProjectMembersPaginatedSchema,
    PaginationMetaSchema
)

# ==========================================
# Get all members by email
# Parameters:
# - email: The email of the user
# - project_id: The ID of the project
# - page: The page number
# - limit: The number of items per page
# Returns:
# - The members
# ==========================================
async def get_members_by_role(
    role: str,
    project_id: str,
    page: int = 1,
    limit: int = 10
) -> WorkspaceProjectMemberSchema:
    
    # ===== Validation and error handling =====
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    
    if not role:
        raise HTTPException(status_code=400, detail="Role is required")
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # ===== Pagination and search =====
    # Pagination offset
    offset = (page - 1) * limit

    members = await WorkspaceProjectMemberModel.find({
        "projectId": project_id,
        "role": role
    }).skip(offset).limit(limit).to_list(length=limit)

    # Get total number of members
    total_members = await WorkspaceProjectMemberModel.find({
        "projectId": project_id,
        "role": role
    }).count()

    # Calculate total pages
    total_pages = (total_members + limit - 1) // limit

    # Meta
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=total_pages,
        totalItems=total_members
    )

    # Items
    items = [
        WorkspaceProjectMemberSchema(
            email=member.email,
            projectId=member.projectId,
            userId=member.userId,
            role=member.role
        ) for member in members
    ]

    return WorkspaceProjectMembersPaginatedSchema(
        meta=meta,
        items=items
    )