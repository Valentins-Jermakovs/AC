# Imports
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
# Models
from ...models import KanbanTaskModel
# Schemas
from ...schemas.response.kanban_task import KanbanTaskSchema


async def create_task(
    title: str, 
    stage_id: str,
    board_id: str, 
    description: Optional[str] = None, 
):
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