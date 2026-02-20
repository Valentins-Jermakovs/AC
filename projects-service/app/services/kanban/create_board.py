# Imports
from fastapi import HTTPException
# Models
from ...models import KanbanBoardModel
# Schemas
from ...schemas.response.kanban_board import KanbanBoardSchema

# Function create a kanban board
# Parameters:
# - title: The title of the board
# - user_id: The ID of the user who created the board

async def create_board(title: str, user_id: str):

    # remove space from title
    title = title.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")

    # Create new board
    new_board = KanbanBoardModel(
        userId=user_id,
        title=title
    )

    # Save new document in MongoDb
    await new_board.save()

    # Return new board
    return KanbanBoardSchema(
        id=str(new_board.id),              # ObjectId -> str
        title=new_board.title,
        createdAt=new_board.createdAt
    )