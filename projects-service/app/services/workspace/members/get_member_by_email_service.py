# Imports
from fastapi import HTTPException
from bson import ObjectId
import re
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
async def get_member_by_email(
    email: str,
    project_id: str,
    page: int = 1,
    limit: int = 10
) -> WorkspaceProjectMembersPaginatedSchema:
    
    # ===== Validation and error handling =====
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Normalize
    email = email.strip().lower()
    
    # Validate email format
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(regex, email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )
    
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    

    # ===== Find all members by email =====
    # Pagination offset
    offset = (page - 1) * limit
    
    member = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "email": email
    })

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Meta
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=1,
        totalItems=1
    )

    # Item
    item = WorkspaceProjectMemberSchema(
        email=member.email,
        role=member.role,
        userId=member.userId,
        projectId=member.projectId
    )

    # ===== Return all members =====
    return WorkspaceProjectMembersPaginatedSchema(
        meta=meta,
        items=[item]
    )