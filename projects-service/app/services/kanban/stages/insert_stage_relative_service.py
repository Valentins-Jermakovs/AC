from fastapi import HTTPException
from bson import ObjectId
from app.models import KanbanStageModel
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

async def insert_stage_relative(
    board_id: str,
    title: str,
    reference_stage_id: str, # stage which will be used as reference
    position: str  # "before" or "after"
) -> KanbanStageSchema:
    
    if board_id is None:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if title is None:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")

    if reference_stage_id is None:
        raise HTTPException(status_code=400, detail="Reference stage ID is required")
    
    if not ObjectId.is_valid(reference_stage_id):
        raise HTTPException(status_code=400, detail="Invalid reference stage ID")

    if position not in ["before", "after"]:
        raise HTTPException(status_code=400, detail="Position must be 'before' or 'after'")

    # if title not unique
    # Find stage with user_id and title
    stage = await KanbanStageModel.find_one({
        "title": title,
        "boardId": board_id
    })
    if stage:
        raise HTTPException(status_code=400, detail="Title must be unique")

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