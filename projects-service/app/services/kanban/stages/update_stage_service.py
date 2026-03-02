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
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # if title not unique
    # Find stage with user_id and title
    stage = await KanbanStageModel.find_one({
        "boardId": board_id,
        "title": title
    })
    if stage:
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")

    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")
    
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
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