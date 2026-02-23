# Imports
from fastapi import HTTPException
import re
# Models
from ...models import KanbanBoardModel
# Schemas
from ...schemas.response.kanban_board import KanbanBoardSchema
from ...schemas.response.kanban_boards_paginated import PaginationMeta

# Find board by title
async def find_board_by_title(
    title: str, 
    user_id: str,
    limit: int = 10,
    page: int = 1
):

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
    meta = PaginationMeta(
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

    return {
        "items": items,
        "meta": meta
    }