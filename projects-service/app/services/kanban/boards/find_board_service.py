# Imports
from fastapi import HTTPException
import re
# Models
from app.models import KanbanBoardModel
# Schemas
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema
from app.schemas.response.kanban.boards.kanban_boards_paginated_schema import KanbanBoardsPaginatedSchema, PaginationMetaSchema

# =============================
# Find board by title
# =============================
async def find_board_by_title(
    title: str, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> KanbanBoardsPaginatedSchema:

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Raise if title is not provided
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # Raise if limit is not a positive integer
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    # Raise if page is not a positive integer
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")

    # Pagination offset
    offset = (page - 1) * limit

    # Try to find board by title
    total_boards = await KanbanBoardModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).count()

    if total_boards == 0:
        raise HTTPException(status_code=404, detail="Board not found")
    
    if offset >= total_boards:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Try to find board by title and user_id
    boards = await KanbanBoardModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        total_pages=(total_boards + limit - 1) // limit,
        total_items=total_boards
    )

    items = [
        KanbanBoardSchema(
            id=str(board.id),
            title=board.title,
            createdAt=board.createdAt
        ) for board in boards
    ]

    return KanbanBoardsPaginatedSchema(
        items=items,
        meta=meta
    )
