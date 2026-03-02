# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

# ===================================
# Function get all stages by board id
# ===================================
async def get_all_stages(
    board_id: str
) -> dict:
    if board_id is None:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    stages = await KanbanStageModel.find({
        "boardId": board_id
    }).sort("order").to_list()

    items = [
        KanbanStageSchema(
            id=str(stage.id),
            title=stage.title,
            order=stage.order,
            createdAt=stage.createdAt
        ) for stage in stages
    ]

    return {
        "items": items
    }