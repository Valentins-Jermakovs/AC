from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanStageModel

async def delete_stage(
    stage_id: str
):
    # Find stage
    stage = await KanbanStageModel.find_one({
        "_id": ObjectId(stage_id)
    })

    # Raise if stage not found
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Delete stage
    await stage.delete()

    return {"message": f"Stage '{stage.title}' deleted successfully"}