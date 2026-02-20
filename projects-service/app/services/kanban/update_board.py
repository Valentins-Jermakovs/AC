# Imports
from bson import ObjectId
from fastapi import HTTPException
# Models
from ...models import KanbanBoardModel
# Schemas
from ...schemas.response.kanban_board import KanbanBoardSchema

async def update_board(board_id: str, title: str):
    
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
