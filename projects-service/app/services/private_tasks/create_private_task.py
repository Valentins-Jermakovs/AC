from ...schemas.response.private_task import PrivateTaskSchema
from ...schemas.data.private_task_create import PrivateTaskCreateSchema
from ...models import PrivateTaskModel

from ...utils.time_converter import convert_to_datetime

async def create_private_task(data: PrivateTaskCreateSchema, user_id: str):
    
    # Convert dueDate string to datetime (if exists)
    due_date_dt = await convert_to_datetime(data.dueDate)

    # Create new private task
    new_private_task = PrivateTaskModel(
        userId=user_id,
        title=data.title,
        description=data.description,
        dueDate=due_date_dt
    )
    
    # Save new document in MongoDb
    await new_private_task.save()

    return PrivateTaskSchema(
        id=str(new_private_task.id),              # ObjectId -> str
        title=new_private_task.title,
        description=new_private_task.description,
        createdAt=new_private_task.createdAt,
        dueDate=new_private_task.dueDate,
        completed=new_private_task.completed
    )
