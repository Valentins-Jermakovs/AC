# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import KanbanBoardMemberModel


# =================================================
# Delete board member
# =================================================
async def delete_board_member(
    board_id: str,
    user_id: str,
    user_id_creator: str
) -> dict:

    # ================= VALIDATION =================

    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    # ================= VERIFY CREATOR =================

    creator = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id_creator
    })

    if not creator:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this board"
        )

    if creator.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=403,
            detail="Only admin or owner can remove members"
        )

    # ================= BLOCK SELF REMOVAL =================

    if user_id_creator == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove yourself"
        )

    # ================= FIND MEMBER TO DELETE =================

    board_member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    if not board_member:
        raise HTTPException(
            status_code=404,
            detail="Board member not found"
        )

    # ================= ROLE PROTECTION =================

    # Admin cannot remove owner
    if creator.role == "admin" and board_member.role == "owner":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot remove owner"
        )

    # ================= DELETE =================

    await board_member.delete()

    return {"message": "Board member removed successfully"}