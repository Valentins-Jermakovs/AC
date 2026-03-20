# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== Tasks Schemas =====
# ===== data:
from app.schemas.data.private_tasks.private_task_create_schema import PrivateTaskCreateSchema
from app.schemas.data.private_tasks.private_task_update_schema import PrivateTaskUpdateSchema
from app.schemas.data.private_tasks.private_task_remove_schema import PrivateTaskRemoveSchema
# ===== response:
from app.schemas.response.private_tasks.private_task import PrivateTaskSchema
from app.schemas.response.private_tasks.private_tasks_paginated import PaginatedPrivateTasksSchema
# =========================
# Utils
from app.utils.check_access_token import check_access_token
# Services
# ====== Tasks Services ======
from app.services.private_tasks.create_private_task_service import create_private_task
from app.services.private_tasks.read_tasks_paginated_service import get_all_private_tasks_paginated
from app.services.private_tasks.find_task_service import (
    find_task_by_title, 
    find_task_by_description, 
    find_task_by_duedate, 
    find_task_by_month
)
from app.services.private_tasks.update_private_task_service import update_private_task
from app.services.private_tasks.remove_private_task_service import remove_private_task
from app.services.private_tasks.get_all_tasks_service import (
    get_all_private_tasks_counted, 
    get_all_private_completed_tasks_counted, 
    get_all_private_tasks_by_current_month, 
    get_all_private_completed_tasks_by_current_month
)
# ===========================

# Router
router = APIRouter(
    prefix="/private-tasks",
    tags=["Private tasks management service"]
)

# Security scheme for access token
security = HTTPBearer()


# ===== Tasks GET ==========================================================
# Route for all tasks (paginated)
@router.get(
    "/get-all-tasks",
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

    return await get_all_private_tasks_paginated(
        page=page, 
        limit=limit, 
        user_id=user_id
    )

# Route for find tasks by title
@router.get(
    "/get-tasks-by-title",
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

    return await find_task_by_title(
        title=title, 
        user_id=user_id, 
        page=page, 
        limit=limit
    )

# Rote for find task by description
@router.get(
    "/get-tasks-by-description",
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

    return await find_task_by_description(
        description=description, 
        user_id=user_id, 
        page=page, 
        limit=limit
    )

# Find task by due date
@router.get(
    "/get-tasks-by-duedate",
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

    return await find_task_by_duedate(
        due_date=due_date, 
        user_id=user_id, 
        page=page, 
        limit=limit
    )

# Find task by month
@router.get(
    "/get-tasks-by-month",
    response_model=PaginatedPrivateTasksSchema,
)
async def find_tasks_by_month_endpoint(
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

    return await find_task_by_month( 
        month=month, 
        user_id=user_id, 
        page=page, 
        limit=limit
    )

# Get all tasks
@router.get(
    "/get-all-tasks-counted",
)
async def get_all_tasks_counted_endpoint(
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all tasks from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all tasks from DB
    4. Return all tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_private_tasks_counted(user_id=user_id)

# Get all tasks completed
@router.get(
    "/get-all-tasks-completed-counted",
)
async def get_all_tasks_completed_counted_endpoint(
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all tasks from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all tasks from DB
    4. Return all tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_private_completed_tasks_counted(user_id=user_id)

# Get all tasks in current month
@router.get(
    "/get-all-tasks-current-month-counted",
)
async def get_all_tasks_current_month_counted_endpoint(
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all tasks from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all tasks from DB
    4. Return all tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_private_tasks_by_current_month(user_id=user_id)

# Get all tasks in current month completed
@router.get(
    "/get-all-tasks-current-month-completed-counted",
)
async def get_all_tasks_current_month_completed_counted_endpoint(
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all tasks from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all tasks from DB
    4. Return all tasks
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_private_completed_tasks_by_current_month(user_id=user_id)


# ===== Tasks POST ==========================================================
# Route for creating a new private task
@router.post(
    "/create-task",
    response_model=PrivateTaskSchema
)
async def create_private_task_endpoint(
    data: PrivateTaskCreateSchema,
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

    return await create_private_task(
        data=data, 
        user_id=user_id
    )

# ===== Tasks PUT ==========================================================
# Route for update a task by _id
@router.put(
    "/update-task",
    response_model=PrivateTaskSchema
)
async def update_private_task_endpoint(
    data: PrivateTaskUpdateSchema,
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

    return await update_private_task(
        task_id=data.taskId, 
        title=data.title, 
        description=data.description, 
        dueDate=data.dueDate, 
        completed=data.completed
    )

# ===== Tasks DELETE ==========================================================
# Route for remove a task by _id
@router.delete(
    "/delete-task",
)
async def remove_private_task_endpoint(
    data: PrivateTaskRemoveSchema,
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

    return await remove_private_task(
        task_id=data.taskId, 
        user_id=user_id
    )