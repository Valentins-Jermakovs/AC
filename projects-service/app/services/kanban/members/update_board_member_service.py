# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel

# =================================================
# Update board member
# Parameters:
# - board_id: The ID of the board
# - user_id: The ID of the user
# - role: The role of the user
# Returns:
# - Message
# =================================================
async def update_board_member(
    board_id: str, 
    user_id: str, 
    role: str
) -> dict:

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Raise if board_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
    role = role.lower().strip()
    if not role:
        raise HTTPException(status_code=400, detail="Role is required")

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