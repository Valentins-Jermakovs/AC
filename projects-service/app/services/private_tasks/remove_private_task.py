from fastapi import HTTPException
from bson import ObjectId
from ...models import PrivateTaskModel

async def remove_private_task(task_id: str, user_id: str):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # try to find task by user_id and task_id
    task = await PrivateTaskModel.find_one({
        "_id": ObjectId(task_id), 
        "userId": user_id
    })

    # Raise if task not found
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Remove task
    await task.delete()
    
    return {"message": f"Private task '{task.title}' removed successfully"}