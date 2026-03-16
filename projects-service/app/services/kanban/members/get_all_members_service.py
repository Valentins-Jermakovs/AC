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
# Get all members by board_id
# Parameters:
# - board_id: The ID of the board
# - page: The page number
# - limit: The number of items per page
# Returns:
# - The members
# ==========================================
async def get_all_members(
    board_id: str,
    user_id: str,
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
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # ===== Current user handling =====
    # Check role of current user
    user = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not a member of this board")

    if user.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="Only owner or admin can view members")


    # ===== Data handling =====
    # Pagination offset
    offset = (page - 1) * limit

    # Count total members
    total_members = await KanbanBoardMemberModel.find({
        "boardId": board_id
    }).count()

    if total_members == 0:
        raise HTTPException(status_code=404, detail="Members not found")
    
    if offset >= total_members:
        raise HTTPException(status_code=404, detail="Page not found")

    # Try to find members by board_id
    members = await KanbanBoardMemberModel.find({
        "boardId": board_id
    }).skip(offset).limit(limit).to_list()

    # ===== Data handling =====
    items = [
        KanbanBoardMemberSchema(
            id=str(member.id),
            email=member.email,
            boardId=member.boardId,
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

    return KanbanBoardMembersPaginatedSchema(
        items=items,
        meta=meta
    )