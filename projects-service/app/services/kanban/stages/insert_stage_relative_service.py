# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel, KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

# ==========================
# Insert a new kanban stage
# ==========================
async def insert_stage_relative(
    board_id: str,
    title: str,
    reference_stage_id: str, # stage which will be used as reference
    position: str,  # "before" or "after"
    user_id: str
) -> KanbanStageSchema:
    
    # ===== Validation and error handling =====
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

    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    # ===== Current user handling =====
    # Check role of current user
    user = await KanbanBoardMemberModel.find_one({
        "boardId": board_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(status_code=403, detail="You are not member of this board or this board does not exist")
    
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="You cannot create stage in this board")


    # if title not unique
    # Find stage with the same title except this one
    stage = await KanbanStageModel.find_one({
        "title": title,
        "boardId": board_id,
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