# Imports
from fastapi import HTTPException
# Models
from ...models import KanbanStageModel
# Schemas
from ...schemas.response.kanban_stage import KanbanStageSchema

# Function get all stages by board id
async def get_all_stages(
    board_id: str
):
    stages = await KanbanStageModel.find({
        "boardId": board_id
    }).sort("order").to_list()

    items = [
        KanbanStageSchema(
            id=str(stage.id),
            title=stage.title,
            order=stage.order,
            createdAt=stage.createdAt
        ) for stage in stages
    ]

    return {
        "items": items
    }