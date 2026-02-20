# Imports
from fastapi import HTTPException
from bson import ObjectId
import re
from datetime import datetime, timedelta
import calendar
# Models
from ...models import PrivateTaskModel
# Schemas
from ...schemas.response.private_task import PrivateTaskSchema
from ...schemas.response.private_tasks_paginated import PaginationMeta
# Utils
from ...utils.time_converter import convert_to_datetime


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

# Find task by description
async def find_task_by_description(
        description: str, 
        user_id: str,
        limit: int = 10,
        page: int = 1
    ):
    
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

# Find task by due date
async def find_task_by_duedate(
        due_date: str, 
        user_id: str,
        limit: int = 10,
        page: int = 1
    ):

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

# Find task by month
async def find_task_by_month(
        year: int,
        month: int, 
        user_id: str,
        limit: int = 10,
        page: int = 1
    ):

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