# Imports
from fastapi import HTTPException
from bson import ObjectId
import re
# Models
from ...models import PrivateTaskModel
# Schemas
from ...schemas.response.private_task import PrivateTaskSchema
from ...schemas.response.private_tasks_paginated import PaginationMeta


# Find task by title
async def find_task_by_title(
        title: str, 
        user_id: str,
        limit: int = 10,
        page: int = 1
    ):
    # Pagination offset
    offset = (page - 1) * limit

    # Count total tasks
    total_tasks = await PrivateTaskModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).count()

    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")
    
    if offset >= total_tasks:
        raise HTTPException(status_code=404, detail="Page not found")

    # Try to find task by title and user_id
    tasks = await PrivateTaskModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_pages=(total_tasks + limit - 1) // limit,
        total_items=total_tasks
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

    return {
        "items": items,
        "meta": meta
    }