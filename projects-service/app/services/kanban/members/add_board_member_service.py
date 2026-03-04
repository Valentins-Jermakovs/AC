# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.members.kanban_board_member_schema import KanbanBoardMemberSchema

# ==================================================
# Function add board member
# Parameters:
# - board_id: The ID of the board
# - user_id: The ID of the user
# - role: The role of the user
# Returns:
# - The board member
# ==================================================
async def add_board_member(
    board_id: str,
    user_id: str,
    role: str,
) -> KanbanBoardMemberSchema:
    """
    Adds a board member to a kanban board.

    Steps:
    1. Create a new board member object
    2. Add the board member to the database
    3. Return the board member

    :param board_id: The ID of the board
    :param user_id: The ID of the user
    :param role: The role of the user
    :param db: The database session
    :return: The board member
    :raises HTTPException: 404 if board or user not found
    """
    role = role.lower().strip()
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    if not role:
        raise HTTPException(status_code=400, detail="Role is required")
    
    if role not in ["viewer", "editor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    board_member = KanbanBoardMemberModel(
        boardId=board_id,
        userId=user_id,
        role=role
    )

    await board_member.save()

    return board_member