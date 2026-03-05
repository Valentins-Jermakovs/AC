# Imports
from fastapi import HTTPException
import re
from datetime import datetime
import calendar
# Models
from app.models import PrivateTaskModel
# Schemas
# =====:response
from app.schemas.response.private_tasks.private_task import PrivateTaskSchema
from app.schemas.response.private_tasks.private_tasks_paginated import (
    PaginatedPrivateTasksSchema,
    PaginationMetaSchema
)
# Utils
from app.utils.time_converter import convert_to_datetime

# ========================
# Find task by title
# ========================
async def find_task_by_title(
    title: str, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> PaginatedPrivateTasksSchema:

    # Raise if title is not provided
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    # Pagination offset
    offset = (page - 1) * limit

    # Count total tasks
    total_tasks = await PrivateTaskModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).count()

    # Raise 404 if dont find any tasks
    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")
    # Raise 404 if requested page exceeds total tasks
    if offset >= total_tasks:
        raise HTTPException(status_code=404, detail="Page not found")
    # Raise if limit > 100
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")
    # Raise if page <= 0
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    # Raise if limit <= 0
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")

    # Try to find task by title and user_id
    tasks = await PrivateTaskModel.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit,
        totalItems=total_tasks
    )

    # Build response
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

    # Return response object
    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )


# ========================
# Find task by description
# ========================
async def find_task_by_description(
    description: str, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> PaginatedPrivateTasksSchema:
    
    # Raise if description is not provided
    if not description:
        raise HTTPException(status_code=400, detail="Description is required")

    # Pagination offset
    offset = (page - 1) * limit

    # Count total tasks
    total_tasks = await PrivateTaskModel.find({
        "description": {"$regex": re.escape(description), "$options": "i"},
        "userId": user_id
    }).count()

    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")
    
    if offset >= total_tasks:
        raise HTTPException(status_code=404, detail="Page not found")

    # Try to find task by description and user_id
    tasks = await PrivateTaskModel.find({
        "description": {"$regex": re.escape(description), "$options": "i"},
        "userId": user_id
    }).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totaPages=(total_tasks + limit - 1) // limit,
        totalItems=total_tasks
    )

    # Build response
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

    # Return response object
    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )

# ========================
# Find task by due date
# ========================
async def find_task_by_duedate(
    due_date: str, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> PaginatedPrivateTasksSchema:

    # Raise if due_date is not provided
    if not due_date:
        raise HTTPException(status_code=400, detail="Due date is required")

    # Pagination offset
    offset = (page - 1) * limit

    # Convert due_date string to datetime
    try:
        due_date_dt = await convert_to_datetime(due_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    # Query: tasks for this user on this due date
    query = {
        "userId": user_id,
        "dueDate": due_date_dt
    }

    # Count total tasks
    total_tasks = await PrivateTaskModel.find(query).count()
    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")

    if offset >= total_tasks:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Fetch tasks for current page
    tasks = await PrivateTaskModel.find(query).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit,
        totalItems=total_tasks
    )

    # Build response
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

    # Return response object
    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )

# ========================
# Find task by month
# ========================
async def find_task_by_month(
    year: int,
    month: int, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> PaginatedPrivateTasksSchema:

    # ===== Validation and error handling =====
    # Raise if limit or page not provided
    if not limit or not page:
        raise HTTPException(status_code=400, detail="Limit and page are required")
    
    # Raise if limit is not a positive integer
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")
    
    # Raise if page is not a positive integer
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    
    # Raise if limit is greater than 100
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")

    # Raise if user id not provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Raise if year or month is not provided
    if not year or not month:
        raise HTTPException(status_code=400, detail="Year and month are required")

    # Pagination offset
    offset = (page - 1) * limit

    # Check valid month
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be 1-12.")
    
    # Star and end datetime for the month
    start_date = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59, 999999)

    # Query task
    query = {
        "userId": user_id,
        "dueDate": {"$gte": start_date, "$lte": end_date}
    }

    # Count total tasks
    total_tasks = await PrivateTaskModel.find(query).count()
    if total_tasks == 0:
        raise HTTPException(status_code=404, detail="Tasks not found")

    if offset >= total_tasks:
        raise HTTPException(status_code=404, detail="Page not found")

    # Fetch tasks for current page
    tasks = await PrivateTaskModel.find(query).skip(offset).limit(limit).to_list()

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit,
        totalItems=total_tasks
    )

    # Build response
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

    # Return response object
    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )