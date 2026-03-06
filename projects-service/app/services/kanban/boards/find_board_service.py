# Imports
from fastapi import HTTPException
import re
from bson import ObjectId
# Models
from app.models import KanbanBoardModel, KanbanBoardMemberModel
# Schemas
# ===== response:
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

    # ===== Validation =====
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")

    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")

    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be positive")

    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be positive")

    offset = (page - 1) * limit

    # ===== Get board ids from member collection =====
    members = await KanbanBoardMemberModel.find({
        "userId": user_id
    }).to_list()

    if not members:
        raise HTTPException(status_code=404, detail="Boards not found")

    board_ids = [ObjectId(member.boardId) for member in members]

    # ===== Count matching boards =====
    total_boards = await KanbanBoardModel.find({
        "_id": {"$in": board_ids},
        "title": {"$regex": re.escape(title), "$options": "i"}
    }).count()

    if total_boards == 0:
        raise HTTPException(status_code=404, detail="Board not found")

    if offset >= total_boards:
        raise HTTPException(status_code=404, detail="Page not found")

    # ===== Get boards =====
    boards = await KanbanBoardModel.find({
        "_id": {"$in": board_ids},
        "title": {"$regex": re.escape(title), "$options": "i"}
    }).skip(offset).limit(limit).to_list()

    # ===== Pagination meta =====
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_boards + limit - 1) // limit,
        totalItems=total_boards
    )

    # ===== Build response =====
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
