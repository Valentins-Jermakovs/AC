# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.members.kanban_board_member_schema import KanbanBoardMemberSchema
from app.schemas.response.kanban.members.kanban_board_members_paginated_schema import (
    KanbanBoardMembersPaginatedSchema, 
    PaginationMetaSchema
)

# ==========================================
# Get all members by email
# Parameters:
# - email: The email of the user
# - board_id: The ID of the board
# - page: The page number
# - limit: The number of items per page
# Returns:
# - The members
# ==========================================
async def get_members_by_role(
    role: str,
    board_id: str,
    page: int = 1,
    limit: int = 10
) -> KanbanBoardMembersPaginatedSchema:
    
    # ===== Validation and error handling =====
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    
    if not role:
        raise HTTPException(status_code=400, detail="Role is required")
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    # ===== Pagination and search =====
    # Pagination offset
    offset = (page - 1) * limit

    members = await KanbanBoardMemberModel.find({
        "boardId": board_id,
        "role": role
    }).skip(offset).limit(limit).to_list(length=limit)

    # Get total number of members
    total_members = await KanbanBoardMemberModel.find({
        "boardId": board_id,
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
        KanbanBoardMemberSchema(
            email=member.email,
            boardId=member.boardId,
            userId=member.userId,
            role=member.role
        ) for member in members
    ]

    return KanbanBoardMembersPaginatedSchema(
        meta=meta,
        items=items
    )