# Imports
from fastapi import HTTPException
# Models
from app.models import PrivateTaskModel
# Schemas
#===== response:
from app.schemas.response.private_tasks.private_tasks_paginated import (
    PaginationMetaSchema,
    PaginatedPrivateTasksSchema
)
from app.schemas.response.private_tasks.private_task import PrivateTaskSchema

'''
    Get all private tasks from the database

    Steps:
    1. Get all private tasks from the database
    2. Return paginated tasks
'''

# =======================================
# Get all private tasks from the database
# =======================================
async def get_all_private_tasks_paginated(
    page: int = 1,
    limit: int = 10,
    user_id: str = None
):
    # ===== Validation and error handling =====
    # Raise if user id not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Raise if limit is not a positive integer
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    # Raise if page is not a positive integer
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    # Raise if limit is greater than 100
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")

    # ===== Data handling =====
    # Pagination offset
    offset = (page - 1) * limit

    query = {}      # Query for database

    if user_id:
        query['userId'] = user_id

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Total tasks count
    total_tasks = await PrivateTaskModel.find(query).count()

    # Raise 404 if requested page exceeds total tasks
    if offset >= total_tasks and total_tasks != 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # Raise 404 if dont find any tasks
    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")

    # Fetch tasks for current page using limit & offset
    tasks = (
        await PrivateTaskModel.find(query)
        .skip(offset)
        .limit(limit)
        .to_list(length=limit)
    )

    # Convert to schema
    items = [
        PrivateTaskSchema(
            id=str(task.id),
            title=task.title,
            description=task.description,
            createdAt=task.createdAt,
            dueDate=task.dueDate,
            completed=task.completed
        )
        for task in tasks
    ]

    # Pagination meta
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit,
        totalItems=total_tasks,
    )

    # Return an object
    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )



