# Imports
from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanBoardModel

async def remove_board(board_id: str, user_id: str):

    # Raise if task_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # try to find task by user_id and task_id
    board = await KanbanBoardModel.find_one({
        "_id": ObjectId(board_id),
        "userId": user_id
    })

    # Raise if task not found
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    # Remove task
    await board.delete()
    
    return {"message": f"Board '{board.title}' removed successfully"}