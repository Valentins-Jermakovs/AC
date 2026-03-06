# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import KanbanStageModel, KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

# =========================
# Create a new kanban stage
# =========================
async def create_stage(
    board_id: str,
    title: str,
    user_id: str
) -> KanbanStageSchema:
    
    # ===== Validation and error handling =====
    # Raise if title is empty
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
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

    # Raise if board_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    
    if not user_id:
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
    # Find stage with equial title except current
    stage = await KanbanStageModel.find_one({
        "boardId": board_id,
        "title": title
    })

    if stage:
        raise HTTPException(status_code=400, detail="Title must be unique")

    # Find last stage in board
    last_stage = await KanbanStageModel.find({
        "boardId": board_id
    }).sort("-order").first_or_none()

    # If stages not exist
    if not last_stage:
        new_order = 1000.0
    else:
        new_order = last_stage.order + 1000.0

    # Create stage
    stage = KanbanStageModel(
        boardId=board_id,
        title=title,
        order=new_order
    )

    # Insert into DB
    await stage.insert()

    # Return stage
    return KanbanStageSchema(
        id=str(stage.id),
        title=stage.title,
        order=stage.order,
        createdAt=stage.createdAt
    )