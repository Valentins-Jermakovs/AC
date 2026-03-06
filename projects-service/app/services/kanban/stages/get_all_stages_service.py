# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel, KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

# ===================================
# Function get all stages by board id
# ===================================
async def get_all_stages(
    board_id: str,
    user_id: str
) -> dict:
    
    # ===== Validation and error handling =====
    if board_id is None:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # ===== Current user handling =====
    # Check role of current user
    user = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this board or this board does not exist")

    # Get all stages
    stages = await KanbanStageModel.find({
        "boardId": board_id
    }).sort("order").to_list()

    # Build response
    items = [
        KanbanStageSchema(
            id=str(stage.id),
            title=stage.title,
            order=stage.order,
            createdAt=stage.createdAt
        ) for stage in stages
    ]

    # Return
    return {
        "items": items
    }