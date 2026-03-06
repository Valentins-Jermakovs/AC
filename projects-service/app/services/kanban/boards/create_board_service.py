# Imports
from fastapi import HTTPException
# Models
from app.models import KanbanBoardModel
# Schemas
# ===== response:
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema

# Helper services
from app.services.kanban.members.add_board_member_service import add_board_member

# ===================================================
# Function create a kanban board
# Parameters:
# - title: The title of the board
# - user_id: The ID of the user who created the board
# Returns:
# - The created board
# ===================================================
async def create_board(
    title: str, 
    user_id: str
) -> KanbanBoardSchema:

    # ===== Validation and error handling =====
    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # remove space from title
    title = title.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # Find board with the same title
    board = await KanbanBoardModel.find_one({
        "userId": user_id,
        "title": title,
    })

    if board:
        raise HTTPException(status_code=400, detail="Title must be unique")

    # Create new board
    new_board = KanbanBoardModel(
        userId=user_id,
        title=title
    )

    # Save new document in MongoDb
    await new_board.save()

    # Add user as board member
    await add_board_member(
        board_id=str(new_board.id),
        user_id=user_id,
        role="owner",
        mode="create_owner",
        user_id_creator=user_id
    )

    # Return new board
    return KanbanBoardSchema(
        id=str(new_board.id),              # ObjectId -> str
        title=new_board.title,
        createdAt=new_board.createdAt
    )