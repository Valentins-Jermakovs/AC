# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel


# =================================================
# Delete board member
# Parameters:
# - board_id: The ID of the board
# - user_id: The ID of the user
# Returns:
# - Message
# =================================================
async def delete_board_member(
    board_id: str, 
    user_id: str,
    user_id_creator: str
) -> dict:
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
    if user_id == user_id_creator:
        raise HTTPException(status_code=400, detail="You cannot remove yourself")

    # try to find board by user_id and board_id
    board_member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    # Raise if board not found
    if not board_member:
        raise HTTPException(status_code=404, detail="Board member not found")
    
    # Remove board member
    await board_member.delete()
    
    return {"message": "Board member removed successfully"}