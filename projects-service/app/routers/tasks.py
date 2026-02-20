# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.private_task import PrivateTaskSchema
from ..schemas.response.private_tasks_paginated import PaginatedPrivateTasksSchema
from ..schemas.data.private_task_create import PrivateTaskCreateSchema
from ..schemas.data.private_task_update import PrivateTaskUpdateSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.private_tasks.create_private_task import create_private_task
from ..services.private_tasks.read_tasks_paginated import get_all_private_tasks_paginated
from ..services.private_tasks.update_private_task import update_private_task
from ..services.private_tasks.remove_private_task import remove_private_task
from ..services.private_tasks.find_task import find_task_by_title, find_task_by_description, find_task_by_duedate, find_task_by_month
router = APIRouter(
    prefix="/tasks",
    tags=["Private tasks management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new private task
@router.post(
    "/create",
    summary="Create a new private task",
    description="Get JSON data and create a new private task in the database",
    response_model=PrivateTaskSchema
)
async def create_private_task_endpoint(
    data: Annotated[PrivateTaskCreateSchema,
        Body(
            example={
                "title": "Task title",
                "description": "Task description",
                "dueDate": "2023-05-31"
            }
        )],
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a new private task.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create private task in DB
    4. Return created private task
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    new_private_task = await create_private_task(data, user_id)

    return new_private_task

# Route for all tasks (paginated)
@router.get(
    "/all",
    summary="Get all private tasks",
    description="Get all private tasks from the database",
    response_model=PaginatedPrivateTasksSchema,
)
async def get_all_private_tasks_endpoint(
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all private tasks from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all private tasks from DB
    4. Return all private tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    all_private_tasks = await get_all_private_tasks_paginated(page, limit, user_id)

    return all_private_tasks

# Route for find tasks by title
@router.get(
    "/title",
    summary="Find tasks by title",
    description="Find tasks by title from the database",
    response_model=PaginatedPrivateTasksSchema,
)
async def find_tasks_by_title_endpoint(
    title: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Find tasks by title from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to find tasks by title from DB
    4. Return found tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    found_tasks = await find_task_by_title(title, user_id, page=page, limit=limit)

    return found_tasks

# Rote for find task by description
@router.get(
    "/description",
    summary="Find tasks by description",
    description="Find tasks by description from the database",
    response_model=PaginatedPrivateTasksSchema,
)
async def find_tasks_by_description_endpoint(
    description: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Find tasks by description from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to find tasks by description from DB
    4. Return found tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    found_tasks = await find_task_by_description(description, user_id, page=page, limit=limit)

    return found_tasks

# Find task by due date
@router.get(
    "/duedate",
    summary="Find tasks by due date",
    description="Find tasks by due date from the database",
    response_model=PaginatedPrivateTasksSchema,
)
async def find_tasks_by_duedate_endpoint(
    due_date: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Find tasks by due date from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to find tasks by due date from DB
    4. Return found tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    found_tasks = await find_task_by_duedate(due_date, user_id, page=page, limit=limit)

    return found_tasks

# Find task by month
@router.get(
    "/month",
    summary="Find tasks by month",
    description="Find tasks by month from the database",
    response_model=PaginatedPrivateTasksSchema,
)
async def find_tasks_by_month_endpoint(
    year: int,
    month: int,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Find tasks by month from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to find tasks by month from DB
    4. Return found tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    found_tasks = await find_task_by_month(year=year, month=month, user_id=user_id, page=page, limit=limit)

    return found_tasks

# Route for update a task by _id
@router.put(
    "/update/{task_id}",
    summary="Update a task",
    description="Update a task in the database",
    response_model=PrivateTaskSchema
)
async def update_private_task_endpoint(
    task_id: str,
    data: Annotated[PrivateTaskUpdateSchema, 
        Body(
            example={
                "title": "Task title",
                "description": "Task description",
                "dueDate": "2023-05-31",
                "completed": True
            }
        )
    ],
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update a task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update private task in DB
    4. Return updated private task
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    updated_private_task = await update_private_task(task_id, data.title, data.description, data.dueDate, data.completed)

    return updated_private_task

# Route for remove a task by _id
@router.delete(
    "/remove/{task_id}",
    summary="Remove a task",
    description="Remove a task from the database"
)
async def remove_private_task_endpoint(
    task_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Remove a task from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to remove private task from DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await remove_private_task(task_id, user_id)