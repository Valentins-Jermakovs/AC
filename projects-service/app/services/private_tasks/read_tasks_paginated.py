# Imports
from bson import ObjectId
from fastapi import HTTPException
# Models
from ...models import PrivateTaskModel
# Schemas
from ...schemas.response.private_tasks_paginated import PaginatedPrivateTasksSchema, PaginationMeta
from ...schemas.response.private_task import PrivateTaskSchema

'''
    Get all private tasks from the database

    Steps:
    1. Get all private tasks from the database
    2. Return paginated tasks
'''

async def get_all_private_tasks_paginated(
    page: int = 1,
    limit: int = 10,
    user_id: str = None
):
    # Pagination offset
    offset = (page - 1) * limit

    query = {}

    if user_id:
        query['userId'] = user_id

    # Raise if user_id is not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Total tasks count
    total_tasks = await PrivateTaskModel.find(query).count()

    # Raise 404 if requested page exceeds total tasks
    if offset > total_tasks:
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

    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_pages=total_tasks // limit + 1,
        total_items=total_tasks,
    )

    return {
        "items":items, "meta":meta
    }



