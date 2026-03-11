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

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    offset = (page - 1) * limit

    # Find tasks matching title
    tasks_query = {
        "title": {"$regex": re.escape(title), "$options": "i"},
        "userId": user_id
    }

    total_tasks = await PrivateTaskModel.find(tasks_query).count()

    # Atsakāmies no 404 — ja nav atrasts, vienkārši items = []
    if offset >= total_tasks:
        # Ja page pārsniedz, return tukšu sarakstu
        items = []
    else:
        tasks = await PrivateTaskModel.find(tasks_query).skip(offset).limit(limit).to_list()
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

    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit if total_tasks > 0 else 1,
        totalItems=total_tasks
    )

    return PaginatedPrivateTasksSchema(items=items, meta=meta)


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

    # Query
    query = {
        "description": {"$regex": re.escape(description), "$options": "i"},
        "userId": user_id
    }

    # Count total tasks
    total_tasks = await PrivateTaskModel.find(query).count()

    # Fetch tasks only if offset < total_tasks
    if offset >= total_tasks or total_tasks == 0:
        items = []  # tukšs saraksts, ja nav atrasts vai page pārsniedz
    else:
        tasks = await PrivateTaskModel.find(query).skip(offset).limit(limit).to_list()
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

    # Pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit if total_tasks > 0 else 1,
        totalItems=total_tasks
    )

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

    # Fetch tasks only if offset < total_tasks
    if total_tasks == 0 or offset >= total_tasks:
        items = []  # tukšs saraksts
    else:
        tasks = await PrivateTaskModel.find(query).skip(offset).limit(limit).to_list()
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

    # Build pagination metadata
    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit if total_tasks > 0 else 1,
        totalItems=total_tasks
    )

    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )

# ========================
# Find task by month
# ========================
async def find_task_by_month(
    month: int, 
    user_id: str,
    limit: int = 10,
    page: int = 1
) -> PaginatedPrivateTasksSchema:

    # Validācija
    if not month:
        raise HTTPException(status_code=400, detail="Month is required")
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be 1-12.")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be 1-100")
    if page <= 0:
        raise HTTPException(status_code=400, detail="Page must be positive integer")

    offset = (page - 1) * limit

    # Query by month
    query = {
        "userId": user_id,
        "$expr": { "$eq": [{ "$month": "$dueDate" }, month] }
    }

    total_tasks = await PrivateTaskModel.find(query).count()

    # Ja nav atrasts neviens uzdevums vai page > total_tasks
    if total_tasks == 0 or offset >= total_tasks:
        items = []
    else:
        tasks = await PrivateTaskModel.find(query).skip(offset).limit(limit).to_list()
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

    meta = PaginationMetaSchema(
        page=page,
        limit=limit,
        totalPages=(total_tasks + limit - 1) // limit if total_tasks > 0 else 1,
        totalItems=total_tasks
    )

    return PaginatedPrivateTasksSchema(
        items=items,
        meta=meta
    )