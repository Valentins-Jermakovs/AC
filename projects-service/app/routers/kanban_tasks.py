# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from ..utils.check_access_token import check_access_token
# Schemas
from ..schemas.response.kanban_task import KanbanTaskSchema
from ..schemas.data.kanban_task_create import KanbanTaskCreateSchema
# Serrvices
from ..services.kanban.create_task import create_task

# Router
router = APIRouter(
    prefix="/kanban/tasks",
    tags=["Kanban task management service"]
)

# Security scheme for access token
security = HTTPBearer()

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