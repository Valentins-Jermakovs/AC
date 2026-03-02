# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from ..utils.check_access_token import check_access_token
# Schemas
from ..schemas.response.kanban_task import KanbanTaskSchema
from ..schemas.data.kanban_task_create import KanbanTaskCreateSchema
from ..schemas.data.kanban_task_update import KanbanTaskUpdate
# Serrvices
from ..services.kanban.create_task import create_task
from ..services.kanban.update_task import update_task
from ..services.kanban.task_delete import delete_task
from ..services.kanban.move_task import move_task_in_stage, move_task_between_stages
from ..services.kanban.get_all_tasks import get_all_tasks

# Router
router = APIRouter(
    prefix="/kanban/tasks",
    tags=["Kanban task management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for getting all tasks
@router.get(
    "/all",
    summary="Get all tasks",
    description="Get all tasks from the database",
)
async def get_all_tasks_endpoint(
    stage_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
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

    return await get_all_tasks(stage_id=stage_id)

# Route for creating a new kanban task
@router.post(
    "/create",
    summary="Create a kanban task",
    description="Create a new kanban task in the database",
    response_model=KanbanTaskSchema
)
async def create_task_endpoint(
    data: Annotated[KanbanTaskCreateSchema, 
        Body(example={
            "title": "Task title",
            "stage_id": "stage_id",
            "board_id": "board_id",
            "description": "Task description"
        })],
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new kanban task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create a new kanban task in DB
    4. Return created kanban task
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await create_task(data.title, data.stage_id, data.board_id, data.description)

# Route for update task
@router.put(
    "/update/{task_id}",
    summary="Update a task",
    description="Update a task in the database",
    response_model=KanbanTaskSchema
)
async def update_task_endpoint(
    data: Annotated[KanbanTaskUpdate, 
        Body(example={
            "task_id": "task_id",
            "title": "Task title",
            "description": "Task description"
        })],
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

    return await update_task(data.task_id, data.title, data.description)

# Route for move task in stage
@router.put(
    "/move-in-stage",
    summary="Move a task",
    description="Move a task in the database",
)
async def move_task_endpoint(
    task_id: str,
    direction: str,
    stage_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Move a task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to move task in DB
    4. Return moved task
    """

    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await move_task_in_stage(task_id=task_id, direction=direction, stage_id=stage_id)

# Route for move task between stages
@router.put(
    "/move-between-stages",
    summary="Move a task",
    description="Move a task in the database",
)
async def move_task_between_stages_endpoint(
    task_id: str,
    target_stage_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Move a task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to move task in DB
    4. Return moved task
    """

    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await move_task_between_stages(task_id=task_id, target_stage_id=target_stage_id)

# Route for delete task
@router.delete(
    "/remove/{task_id}",
    summary="Remove a task",
    description="Remove a task from the database"
)
async def remove_task_endpoint(
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

    return await delete_task(task_id)