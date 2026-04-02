# Imports
from fastapi import HTTPException
from datetime import datetime, timezone
# Schemas
from app.schemas.response.private_tasks.private_task import PrivateTaskSchema
from app.schemas.data.private_tasks.private_task_create_schema import PrivateTaskCreateSchema
# Models
from app.models import PrivateTaskModel
# Utils
from app.utils.time_converter import convert_to_datetime

# ========================
# Create private task
# ========================
async def create_private_task(
    data: PrivateTaskCreateSchema, user_id: str
) -> PrivateTaskSchema:
    
    # ===== Validations =====
    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Raise if title is empty
    if not data.title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if data.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    # Raise if title is too long
    if len(data.title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")
    
    # Raise if title is too short
    if len(data.title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    if data.description is not None:
        if data.description.strip() == "":
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        # Raise if description is too long
        if len(data.description) > 1000:
            raise HTTPException(status_code=400, detail="Description is too long")
        # Raise if description is too short
        if len(data.description) < 3:
            raise HTTPException(status_code=400, detail="Description is too short")
    
    # Raise if title is not unique
    # Find task with user_id and title
    task = await PrivateTaskModel.find_one({
        "userId": user_id,
        "title": data.title
    })
    if task:
        raise HTTPException(status_code=400, detail="Title must be unique")


    # Convert dueDate string to datetime (if exists)
    due_date_dt = await convert_to_datetime(data.dueDate)

    # Validate due date is not in the past
    if due_date_dt:
        current_date = datetime.now()

        if due_date_dt < current_date:
            raise HTTPException(
                status_code=400,
                detail="Due date cannot be in the past"
            )

    # Create new private task
    new_private_task = PrivateTaskModel(
        userId=user_id,
        title=data.title,
        description=data.description,
        dueDate=due_date_dt
    )
    
    # Save new document in MongoDb
    await new_private_task.save()

    # Return new private task
    return PrivateTaskSchema(
        id=str(new_private_task.id),              # ObjectId -> str
        title=new_private_task.title,
        description=new_private_task.description,
        createdAt=new_private_task.createdAt,
        dueDate=new_private_task.dueDate,
        completed=new_private_task.completed
    )
