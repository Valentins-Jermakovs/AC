# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from ...models import KanbanTaskModel
# Schemas
from ...schemas.response.kanban_task import KanbanTaskSchema

async def move_task_in_stage(
    task_id: str,
    stage_id: str,
    direction: str  # "up" or "down"
):
    # Get all tasks sorted
    tasks = await KanbanTaskModel.find(
        KanbanTaskModel.stageId == stage_id
    ).sort("order").to_list()

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    # Find index of current task
    task_index = None
    for index, task in enumerate(tasks):
        if str(task.id) == task_id:
            task_index = index
            break

    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Determine target index
    if direction == "up":
        if task_index == 0:
            return {"message": "Already at top"}
        target_index = task_index - 1
    elif direction == "down":
        if task_index == len(tasks) - 1:
            return {"message": "Already at bottom"}
        target_index = task_index + 1
    else:
        raise HTTPException(status_code=400, detail="Invalid direction")

    task = tasks[task_index]
    target_task = tasks[target_index]

    # Proper swap
    task.order, target_task.order = target_task.order, task.order

    # Save changes
    await task.save()
    await target_task.save()

    return {"message": "Task in stage moved successfully"}

# move task between stages
async def move_task_between_stages(
    task_id: str,
    target_stage_id: str,
):
    # Validate task_id
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # Validate target_stage_id
    if not ObjectId.is_valid(target_stage_id):
        raise HTTPException(status_code=400, detail="Invalid target stage ID")

    # Get task
    task = await KanbanTaskModel.find_one({"_id": ObjectId(task_id)})

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get all target tasks
    target_tasks = await KanbanTaskModel.find({
        "stageId": target_stage_id
    }).sort("order").to_list()

    min_order = 0

    if target_tasks:
        min_order = target_tasks[0].order

        for t in target_tasks:
            t.order += 1
            await t.save()
    
    task.stageId = target_stage_id
    task.order = min_order

    await task.save()

    return {"message": "Task moved between stages successfully"}