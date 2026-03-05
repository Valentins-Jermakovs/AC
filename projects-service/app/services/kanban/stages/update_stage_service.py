# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

async def update_stage(
    board_id: str,
    stage_id: str,
    title: str
) -> KanbanStageSchema:
    
    # ===== Validation and error handling =====

    # Raise if title is empty
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    # Raise if title is empty
    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    # Raise if board_id is not provided
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    # Raise if stage_id is not provided
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    # Raise if board_id is not valid
    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")
    # Raise if board_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
    # if title not unique
    # Find stage with equal title except this stage
    stage = await KanbanStageModel.find_one({
        "boardId": board_id,
        "title": title,
        "_id": {"$ne": ObjectId(stage_id)}
    })

    if stage:
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    # ===== Business logic =====

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

    # Save stage to database
    await stage.save()

    # Return stage
    return KanbanStageSchema(
        id=str(stage.id),
        title=stage.title,
        order=stage.order,
        createdAt=stage.createdAt
    )