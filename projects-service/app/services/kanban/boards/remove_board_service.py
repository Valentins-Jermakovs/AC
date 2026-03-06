# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import (
    KanbanBoardModel, 
    KanbanStageModel, 
    KanbanTaskModel, 
    KanbanBoardMemberModel,
)

# ========================================================
# Remove board function
#
# - Removes a kanban board from the database
# - Removes all stages and tasks associated with the board
# - Removes all board members associated with the board
# ========================================================
async def remove_board(board_id: str, user_id: str) -> dict:

    # Check if current user is owner of this board
    if not await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id,
        "role": "owner"
    }):
        raise HTTPException(status_code=403, detail="You are not owner of this board or this board does not exist")

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Raise if board_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    # try to find board by user_id and board_id
    board = await KanbanBoardModel.find_one({
        "_id": ObjectId(board_id),
        "userId": user_id
    })

    # Raise if board not found
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Find all stages and remove them
    await KanbanStageModel.find({
        "boardId": board_id
    }).delete()

    # Find all tasks and remove them
    await KanbanTaskModel.find({
        "boardId": board_id
    }).delete()

    # Find all board members and remove them
    await KanbanBoardMemberModel.find({
        "boardId": board_id
    }).delete()

    # Remove task
    await board.delete()
    
    return {"message": f"Board '{board.title}' removed successfully"}