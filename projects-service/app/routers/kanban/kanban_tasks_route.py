# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from app.utils.check_access_token import check_access_token
# Schemas
# ===== response:
from app.schemas.response.kanban.tasks.kanban_task_schema import KanbanTaskSchema
# ===== data:
from app.schemas.data.kanban.tasks.kanban_task_create_schema import KanbanTaskCreateSchema
from app.schemas.data.kanban.tasks.kanban_task_update_schema import KanbanTaskUpdateSchema
from app.schemas.data.kanban.tasks.kanban_task_move_schema import KanbanTaskMoveSchema
from app.schemas.data.kanban.tasks.kanban_task_move_btw_stages_schema import KanbanTaskMoveBtwStagesSchema
from app.schemas.data.kanban.tasks.kanban_task_remove_schema import KanbanTaskRemoveSchema
# Services
from app.services.kanban.tasks.create_task_service import create_task
from app.services.kanban.tasks.get_all_tasks_service import get_all_tasks
from app.services.kanban.tasks.update_task_service import update_task
from app.services.kanban.tasks.move_task_service import move_task_in_stage, move_task_between_stages
from app.services.kanban.tasks.task_delete_service import delete_task

# Router
router = APIRouter(
    prefix="/kanban/tasks",
    tags=["Kanban task management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== Tasks GET ==========================================================
# Route for getting all tasks
@router.get(
    "/get-all-tasks",
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

    return await get_all_tasks(
        stage_id=stage_id
    )

# ===== Tasks POST ==========================================================
# Route for creating a new kanban task
@router.post(
    "/create-task",
    response_model=KanbanTaskSchema
)
async def create_task_endpoint(
    data: KanbanTaskCreateSchema,
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

    return await create_task(
        title=data.title, 
        stage_id=data.stageId, 
        board_id=data.boardId, 
        description=data.description
    )

# ===== Tasks PUT ==========================================================
# Route for update task
@router.put(
    "/update-task",
    response_model=KanbanTaskSchema
)
async def update_task_endpoint(
    data: KanbanTaskUpdateSchema,
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

    return await update_task(
        task_id=data.taskId, 
        title=data.title, 
        description=data.description
    )

# Route for move task in stage
@router.put(
    "/move-task-in-stage",
)
async def move_task_endpoint(
    data: KanbanTaskMoveSchema,
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

    return await move_task_in_stage(
        task_id=data.taskId, 
        direction=data.direction, 
        stage_id=data.stageId
    )

# Route for move task between stages
@router.put(
    "/move-task-between-stages",
)
async def move_task_between_stages_endpoint(
    data: KanbanTaskMoveBtwStagesSchema,
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

    return await move_task_between_stages(
        task_id=data.taskId, 
        target_stage_id=data.targetStageId
    )

# ===== Tasks DELETE ==========================================================
# Route for delete task
@router.delete(
    "/delete-task",
)
async def remove_task_endpoint(
    data: KanbanTaskRemoveSchema,
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

    return await delete_task(
        task_id=data.taskId
    )