# Imports
from fastapi import HTTPException
from bson import ObjectId
import re
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
async def get_member_by_email(
    email: str,
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
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Validate email format
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(regex, email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    

    # ===== Find all members by email =====
    # Pagination offset
    offset = (page - 1) * limit
    
    member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
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
    item = KanbanBoardMemberSchema(
        email=member.email,
        role=member.role,
        userId=member.userId,
        boardId=member.boardId
    )

    # ===== Return all members =====
    return KanbanBoardMembersPaginatedSchema(
        meta=meta,
        items=[item]
    )