# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel, KanbanTaskModel

# =================================
# Delete a kanban stage from the DB
# =================================
async def delete_stage(
    stage_id: str
) -> dict:
    
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")

    # Find stage
    stage = await KanbanStageModel.find_one({
        "_id": ObjectId(stage_id)
    })

    # Delete tasks
    await KanbanTaskModel.find({
        "stageId": stage_id
    }).delete()

    # Raise if stage not found
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Delete stage
    await stage.delete()

    return {"message": f"Stage '{stage.title}' deleted successfully"}