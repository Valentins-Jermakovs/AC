# Imports
from fastapi import HTTPException
from ...models import KanbanStageModel
from ...schemas.response.kanban_stage import KanbanStageSchema

async def create_stage(
    board_id: str,
    title: str,
):
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

    await stage.insert()

    return KanbanStageSchema(
        id=str(stage.id),
        title=stage.title,
        order=stage.order,
        createdAt=stage.createdAt
    )