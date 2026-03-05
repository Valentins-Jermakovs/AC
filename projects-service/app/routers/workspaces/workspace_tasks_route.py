# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from app.utils.check_access_token import check_access_token
# Schemas
# ===== response:
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema
from app.schemas.response.workspaces.tasks.workspace_task_list_schema import WorkspaceTaskListSchema
# ===== data:
from app.schemas.data.workspace.tasks.workspace_create_task_schema import WorkspaceCreateTaskSchema
from app.schemas.data.workspace.tasks.workspace_delete_task_schema import WorkspaceDeleteTaskSchema
from app.schemas.data.workspace.tasks.workspace_update_task_schema import WorkspaceUpdateTaskSchema
# Services
from app.services.workspace.tasks.create_task_service import create_task
from app.services.workspace.tasks.delete_task_service import delete_task
from app.services.workspace.tasks.update_task_service import update_task
from app.services.workspace.tasks.get_all_tasks_service import get_all_tasks

# Router
router = APIRouter(
    prefix="/workspace/tasks",
    tags=["Workspace task management service"]
)

# Security scheme for access token
security = HTTPBearer()


# ===== Task GET ==========================================================
# Route for getting all tasks
@router.get(
    "/get-all-tasks", 
    response_model=WorkspaceTaskListSchema
)
async def get_all_tasks_route(
    project_id: str,
    stage_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all tasks in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all tasks in DB
    4. Return list of tasks
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_tasks(
        projectId=project_id,
        stageId=stage_id
    )

# ===== Task POST ==========================================================
# Route for creating a task
@router.post(
    "/create-task", 
    response_model=WorkspaceTaskSchema
)
async def create_task_route(
    workspace_task: WorkspaceCreateTaskSchema, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create a new task in DB
    4. Return created task
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_task(
        task_data=workspace_task
    )


# ===== Task PUT ==========================================================
# Route for updating a task
@router.put(
    "/update-task", 
    response_model=WorkspaceTaskSchema
)
async def update_task_route(
    workspace_task: WorkspaceUpdateTaskSchema, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update a task in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update task in DB
    4. Return updated task
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await update_task(
        data=workspace_task
    )

# ===== Task DELETE ==========================================================
# Route for deleting a task
@router.delete(
    "/delete-task", 
)
async def remove_task_route(
    data: WorkspaceDeleteTaskSchema, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Remove a task from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to remove task from DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await delete_task(
        task_id=data.taskId
    )

