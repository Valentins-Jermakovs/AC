# Models
from ...models import KanbanTaskModel
# Schemas
from ...schemas.response.kanban_task import KanbanTaskSchema

async def get_all_tasks(
    stage_id: str
):
    tasks = await KanbanTaskModel.find({
        "stageId": stage_id
    }).sort("order").to_list()

    items = [
        KanbanTaskSchema(
            id=str(task.id),
            title=task.title,
            description=task.description,
            order=task.order,
            stageId=task.stageId
        ) for task in tasks
    ]

    return {
        "items": items
    }
