from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanBoardMemberModel


async def update_board_member(board_id: str, user_id: str, role: str):
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    # try to find board by user_id and board_id
    board_member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    # Raise if board not found
    if not board_member:
        raise HTTPException(status_code=404, detail="Board member not found")

    # Update role
    board_member.role = role
    await board_member.save()

    return {"message": "Board member role updated successfully"}