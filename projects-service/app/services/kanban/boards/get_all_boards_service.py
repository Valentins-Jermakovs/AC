# Imports
from fastapi import HTTPException
# Models
from app.models import KanbanBoardModel
# Schemas
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema
from app.schemas.response.kanban.boards.kanban_boards_paginated_schema import (
    PaginationMetaSchema, KanbanBoardsPaginatedSchema
)

async def get_all_boards_paginated(
    page: int = 1,
    limit: int = 10,
    user_id: str = None
):
    # Raise if limit is not a positive integer
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    # Raise if page is not a positive integer
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    # Raise if limit is greater than 100
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Pagination offset
    offset = (page - 1) * limit

    query = {}

    if user_id:
        query['userId'] = user_id

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Total boards count
    total_boards = await KanbanBoardModel.find(query).count()

    # Raise 404 if requested page exceeds total boards
    if offset >= total_boards:
        raise HTTPException(status_code=404, detail="Page not found")

    # Raise 404 if dont find any boards
    if total_boards == 0:
        raise HTTPException(status_code=404, detail="Boards not found")

    # Fetch boards for current page using limit & offset
    boards = await KanbanBoardModel.find(query).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        total_pages=total_boards // limit,
        total_items=total_boards
    )

    items = [
        KanbanBoardSchema(
            id=str(board.id),
            title=board.title,
            createdAt=board.createdAt
        ) 
        for board in boards
    ]

    return KanbanBoardsPaginatedSchema(
        items=items,
        meta=meta
    )