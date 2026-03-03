# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import WorkspaceStageModel

# ===================================
# Move a workspace stage in the DB
# ===================================
async def move_stage(
    project_id: str,
    stage_id: str,
    direction: str  # "up" or "down"
) -> dict:

    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    
    if direction not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Direction must be 'up' or 'down'")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # Get all stages sorted
    stages = await WorkspaceStageModel.find(
        WorkspaceStageModel.boardId == project_id
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