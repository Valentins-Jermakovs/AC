# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel

# ====================================
# Move a kanban stage in the database
# ====================================
async def move_stage(
    board_id: str,
    stage_id: str,
    direction: str  # "up" or "down"
) -> dict:

    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")

    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    
    if direction not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Direction must be 'up' or 'down'")

    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # Get all stages sorted
    stages = await KanbanStageModel.find(
        KanbanStageModel.boardId == board_id
    ).sort("order").to_list()

    if not stages:
        raise HTTPException(status_code=404, detail="No stages found")

    # Find index of current stage
    stage_index = None
    for index, stage in enumerate(stages):
        if str(stage.id) == stage_id:
            stage_index = index
            break

    if stage_index is None:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Determine target index
    if direction == "up":
        if stage_index == 0:
            return {"message": "Already at top"}
        target_index = stage_index - 1

    elif direction == "down":
        if stage_index == len(stages) - 1:
            return {"message": "Already at bottom"}
        target_index = stage_index + 1

    else:
        raise HTTPException(status_code=400, detail="Invalid direction")

    stage = stages[stage_index]
    target_stage = stages[target_index]

    # Proper swap
    stage.order, target_stage.order = target_stage.order, stage.order

    await stage.save()
    await target_stage.save()

    return {"message": "Stage moved successfully"}