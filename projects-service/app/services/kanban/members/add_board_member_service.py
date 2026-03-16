# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanBoardMemberModel, KanbanBoardModel
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
    email: str,
    board_id: str,
    user_id: str,
    user_id_creator: str,
    mode: str,
    role: str,
) -> KanbanBoardMemberSchema:


    # ===== Validation =====
    if not email:
        raise HTTPException(400, "Email is required")

    if not board_id:
        raise HTTPException(400, "Board ID is required")

    if not user_id:
        raise HTTPException(400, "User ID is required")

    if not role:
        raise HTTPException(400, "Role is required")

    if mode not in ["create_owner", "add"]:
        raise HTTPException(400, "Invalid mode")

    role = role.lower().strip()

    if role not in ["viewer", "editor", "admin", "owner"]:
        raise HTTPException(400, "Invalid role")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(400, "Invalid board ID")
    
    # try to find board
    board = await KanbanBoardModel.find_one({
        "_id": ObjectId(board_id)
    })

    # Raise if board not found
    if not board:
        raise HTTPException(404, "Board not found")
    
    # ===== Create an owner (mode == create_owner) =====
    if mode == "create_owner":
        # Create board member
        board_member = KanbanBoardMemberModel(
            boardId=board_id,
            userId=user_id,
            email=email,
            role="owner"
        )

        # Save board member
        await board_member.save()

        # Return board member
        return board_member
    
    # ===== Verify creator =====

    creator = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id_creator
    })

    if not creator:
        raise HTTPException(403, "You are not a member of this board")

    if creator.role not in ["admin", "owner"]:
        raise HTTPException(403, "You are not admin or owner of this board")
    

    # ===== Block self modification =====

    if user_id_creator == user_id:
        raise HTTPException(400, "You cannot modify yourself")


    # ===== Block owner creation =====

    if role == "owner":
        raise HTTPException(403, "Owner cannot be added")
    
    # ===== Admin restrictions =====

    if creator.role == "admin" and role in ["admin", "owner"]:
        raise HTTPException(403, "Admin cannot assign this role")


    # if user already exists
    if await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id
    }):
        raise HTTPException(status_code=400, detail="Board member already exists")

    # Create board member
    board_member = KanbanBoardMemberModel(
        email=email,
        boardId=board_id,
        userId=user_id,
        role=role
    )

    # Save board member
    await board_member.save()

    # Return board member
    return board_member