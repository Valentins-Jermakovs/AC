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
    user_id_creator: int,
    role: str
) -> dict:

    # ===== Validation =====
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    role = role.lower().strip()

    if role not in ["viewer", "editor", "admin", "owner"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    if role == "owner":
        raise HTTPException(status_code=400, detail="Cannot assign owner role")

    if user_id == str(user_id_creator):
        raise HTTPException(status_code=400, detail="You cannot update yourself")


    # ===== Get current user (who performs update) =====
    current_user = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": str(user_id_creator)
    })

    if not current_user:
        raise HTTPException(status_code=403, detail="You are not a board member")


    # ===== Permission logic =====

    # Admin restrictions
    if current_user.role == "admin":
        if role not in ["viewer", "editor"]:
            raise HTTPException(
                status_code=403,
                detail="Admin can only assign viewer or editor roles"
            )

    # Viewer / editor cannot modify roles
    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update roles"
        )


    # ===== Find member to update =====
    board_member = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    })

    if not board_member:
        raise HTTPException(status_code=404, detail="Board member not found")


    # ===== Update role =====
    board_member.role = role
    await board_member.save()

    return {"message": "Board member role updated successfully"}