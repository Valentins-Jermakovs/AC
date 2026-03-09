# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from app.models import KanbanTaskModel, KanbanBoardMemberModel
# Schemas
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema

# ==================================
# Function create task
# ==================================
async def create_task(
    title: str, 
    stage_id: str,
    board_id: str,
    user_id: str,
    description: Optional[str] = None,
) -> KanbanTaskSchema:
    
    # ===== Validation and error handling =====
    # Raise if stage_id is not provided
    if not stage_id:
        raise HTTPException(status_code=400, detail="Stage ID is required")
    # Raise if board_id is not provided
    if not board_id:
        raise HTTPException(status_code=400, detail="Board ID is required")
    # Raise if stage_id is not valid
    if not ObjectId.is_valid(stage_id):
        raise HTTPException(status_code=400, detail="Invalid stage ID")
    # Raise if board_id is not valid
    if not ObjectId.is_valid(board_id):
        raise HTTPException(status_code=400, detail="Invalid board ID")
    # Check title
    title = title.strip()
    # Raise if title is empty
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    # Raise if title is too long
    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    # Raise if title is too short
    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    

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
        raise HTTPException(status_code=403, detail="You cant create tasks in this board")


    # Find task with user_id and title
    task = await KanbanTaskModel.find_one({
        "stageId": stage_id,
        "title": title
    })
    if task:
        raise HTTPException(status_code=400, detail="Title must be unique")
    
    # ===== Business logic =====

    # Find last task in stage
    last_task = await KanbanTaskModel.find({
        "stageId": stage_id
    }).sort("-order").first_or_none()

    # If tasks not exist
    if not last_task:
        new_order = 1000.0
    else:
        new_order = last_task.order + 1000.0

    # Create task
    task = KanbanTaskModel(
        boardId=board_id,
        stageId=stage_id,
        title=title,
        description=description,
        order=new_order
    )

    # Insert task
    await task.insert()

    # Return task
    return KanbanTaskSchema(
        id=str(task.id),
        title=task.title,
        description=task.description,
        stageId=task.stageId,
        boardId=task.boardId,
        order=task.order
    )