from fastapi import HTTPException
from bson import ObjectId
from ...models import KanbanStageModel
from ...schemas.response.kanban_stage import KanbanStageSchema

async def insert_stage_relative(
    board_id: str,
    title: str,
    reference_stage_id: str, # stage which will be used as reference
    position: str  # "before" or "after"
) -> KanbanStageSchema:
    # Find reference stage
    reference_stage = await KanbanStageModel.find_one({
        "boardId": board_id,
        "_id": ObjectId(reference_stage_id)
    })

    # Raise if stage not found
    if not reference_stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Fing neighbour depending on position
    if position == "after":
        next_stage = await KanbanStageModel.find({
            "boardId": board_id,
            "order": {"$gt": reference_stage.order}
        }).sort("order").first_or_none()

        if next_stage:
            new_order = (next_stage.order + reference_stage.order) / 2
        else:
            new_order = reference_stage.order + 1000.0
    
    elif position == "before":
        prev_stage = await KanbanStageModel.find({
            "boardId": board_id,
            "order": {"$lt": reference_stage.order}
        }).sort("-order").first_or_none()

        if prev_stage:
            new_order = (prev_stage.order + reference_stage.order) / 2
        else:
            new_order = reference_stage.order - 1000.0

    else:
        raise HTTPException(status_code=400, detail="Invalid position")

    # Create new stage
    stage = KanbanStageModel(
        boardId=board_id,
        title=title,
        order=new_order
    )

    await stage.insert()

    return KanbanStageSchema(
        id=str(stage.id),
        title=stage.title,
        order=stage.order,
        createdAt=stage.createdAt
    )