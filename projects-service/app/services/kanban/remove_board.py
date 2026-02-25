# Imports
from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanBoardModel, KanbanStageModel, KanbanTaskModel, KanbanBoardMemberModel

async def remove_board(board_id: str, user_id: str):

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