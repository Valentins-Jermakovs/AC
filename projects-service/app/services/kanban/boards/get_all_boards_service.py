# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardModel, KanbanBoardMemberModel
# Schemas
# ===== :response
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema
from app.schemas.response.kanban.boards.kanban_boards_paginated_schema import (
    PaginationMetaSchema, 
    KanbanBoardsPaginatedSchema
)

async def get_all_boards_paginated(
    page: int = 1,
    limit: int = 10,
    user_id: str = None
):

    # ===== Validation and error handling =====
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")


    # ===== Business logic =====

    # set pagination
    offset = (page - 1) * limit

    # Get members
    members = await KanbanBoardMemberModel.find({
        "userId": user_id
    }).to_list()

    # Get total boards
    total_boards = len(members)

    # ===== Boards validation =====
    if total_boards == 0:
        raise HTTPException(status_code=404, detail="Boards not found")

    if offset >= total_boards:
        raise HTTPException(status_code=404, detail="Page not found")

    # get ids
    board_ids = [ObjectId(member.boardId) for member in members]

    # Get boards
    boards = await KanbanBoardModel.find({
        "_id": {"$in": board_ids}
    }).skip(offset).limit(limit).to_list()

    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_boards + limit - 1) // limit,
        totalItems=total_boards
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