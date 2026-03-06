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
# Get all project members
# ==========================================
async def get_all_project_members(
    project_id: str,
    user_id: str,
    page: int = 1,
    limit: int = 10
) -> WorkspaceProjectMembersPaginatedSchema:

    # ================= VALIDATION =================

    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")

    project_id = ObjectId(project_id)

    # ================= PERMISSION CHECK =================

    current_user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id
    })

    if not current_user:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only owner or admin can view project members"
        )

    # ================= PAGINATION =================

    offset = (page - 1) * limit

    total_members = await WorkspaceProjectMemberModel.find({
        "projectId": project_id
    }).count()

    if total_members == 0:
        raise HTTPException(status_code=404, detail="Members not found")

    if offset >= total_members:
        raise HTTPException(status_code=404, detail="Page not found")

    members = await WorkspaceProjectMemberModel.find({
        "projectId": project_id
    }).skip(offset).limit(limit).to_list()

    # ================= RESPONSE =================

    items = [
        WorkspaceProjectMemberSchema(
            id=str(member.id),
            projectId=member.projectId,
            userId=member.userId,
            role=member.role
        )
        for member in members
    ]

    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_members + limit - 1) // limit,
        totalItems=total_members
    )

    return WorkspaceProjectMembersPaginatedSchema(
        items=items,
        meta=meta
    )