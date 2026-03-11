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
) -> PaginatedPrivateTasksSchema:

    # ===== Validation =====
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be 1-100")
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")

    offset = (page - 1) * limit

    # ===== Data query =====
    query = {"userId": user_id}

    total_tasks = await PrivateTaskModel.find(query).count()

    # Ja page pārsniedz pieejamo vai nav uzdevumu, items = []
    if total_tasks == 0 or offset >= total_tasks:
        items = []
    else:
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

    # Pagination meta
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit if total_tasks > 0 else 1,
        totalItems=total_tasks,
    )

    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )



