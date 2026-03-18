# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.members.kanban_board_member_schema import KanbanBoardMemberSchema

# ==========================================
# Get current user
# Parameters:
# - user_id: The ID of the user
# - board_id: The ID of the board
# Returns:
# - The current user
# ==========================================
async def get_current_user(
    board_id: str,
    user_id: str
) -> KanbanBoardMemberSchema:

    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    board_member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    if not board_member:
        raise HTTPException(status_code=404, detail="Board member not found")

    return KanbanBoardMemberSchema(
        email=board_member.email,
        role=board_member.role,
        boardId=board_member.boardId,
        userId=board_member.userId
    )