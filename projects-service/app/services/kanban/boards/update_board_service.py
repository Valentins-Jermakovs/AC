# Imports
from bson import ObjectId
from fastapi import HTTPException
# Models
from app.models import KanbanBoardModel
# Schemas
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema

async def update_board(board_id: str, title: str) -> KanbanBoardSchema:
    
    # Raise if id not exist
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    # Raise if task_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    # Check title
    title = title.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")

    # Raise, if title not unique
    # Find board with user_id and title
    board = await KanbanBoardModel.find_one({
        "title": title,
        "userId": board_id
    })
    if board:
        raise HTTPException(status_code=400, detail="Title must be unique")

    # Get board
    board = await KanbanBoardModel.find_one({"_id": ObjectId(board_id)})

    # Raise if board not found
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    updated_data = {
        "title": title
    }

    # Update board
    await board.set(updated_data)

    # Return updated board
    return KanbanBoardSchema(
        id=str(board.id),              # ObjectId -> str
        title=board.title,
        createdAt=board.createdAt
    )
