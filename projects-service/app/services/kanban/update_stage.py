from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanStageModel
from ...schemas.response.kanban_stage import KanbanStageSchema

async def update_stage(
    board_id: str,
    stage_id: str,
    title: str
):
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    # Find stage
    stage = await KanbanStageModel.find_one({
        "boardId": board_id,
        "_id": ObjectId(stage_id)
    })

    # Raise if stage not found
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Update stage
    stage.title = title

    await stage.save()

    return KanbanStageSchema(
        id=str(stage.id),
        title=stage.title,
        order=stage.order,
        createdAt=stage.createdAt
    )