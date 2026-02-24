from fastapi import HTTPException

from bson import ObjectId
from ...models import KanbanBoardMemberModel

from ...schemas.response.kanban_board_member import KanbanBoardMemberSchema
from ...schemas.response.kanban_board_members_paginated import PaginationMeta, KanbanBoardMembersPaginatedSchema

async def get_all_members(
    board_id: str,
    page: int = 1,
    limit: int = 10,
):

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

    items = [
        KanbanBoardMemberSchema(
            id=str(member.id),
            boardId=member.boardId,
            userId=member.userId,
            role=member.role
        )
        for member in members
    ]

    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_pages=(total_members + limit - 1),
        total_items=total_members
    )

    return {
        "items": items,
        "meta": meta
    }