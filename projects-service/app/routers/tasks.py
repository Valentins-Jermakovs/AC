# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.private_task import PrivateTaskSchema
from ..schemas.response.private_tasks_paginated import PaginatedPrivateTasksSchema
from ..schemas.data.private_task_create import PrivateTaskCreateSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.private_tasks.create_private_task import create_private_task
from ..services.private_tasks.read_tasks_paginated import get_all_private_tasks_paginated

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

# Route for tasks pagination
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
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    all_private_tasks = await get_all_private_tasks_paginated(page, limit, user_id)

    return all_private_tasks

