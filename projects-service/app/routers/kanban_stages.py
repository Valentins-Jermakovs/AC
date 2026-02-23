# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.kanban_stage import KanbanStageSchema
from ..schemas.response.all_kanban_stages import AllKanbanStagesSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.kanban.kanban_stage_create import create_stage
from ..services.kanban.get_all_stages import get_all_stages
from ..services.kanban.update_stage import update_stage
from ..services.kanban.delete_stage import delete_stage

# Router
router = APIRouter(
    prefix="/kanban",
    tags=["Kanban stage management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new kanban stage
@router.post(
    "/stage",
    summary="Create a new kanban stage",
    description="Create a new kanban stage in the database",
    response_model=KanbanStageSchema
)
async def create_stage_endpoint(
    board_id: str,
    title: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new kanban stage in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create a new kanban stage in DB
    4. Return created kanban stage
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await create_stage(board_id, title)

# Route for getting all kanban stages
@router.get(
    "/stages",
    summary="Get all kanban stages",
    description="Get all kanban stages from the database",
    response_model=AllKanbanStagesSchema
)
async def get_all_stages_endpoint(
    board_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all kanban stages from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all kanban stages from DB
    4. Return all kanban stages
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_stages(board_id)

# Route for updating a kanban stage
@router.put(
    "/stage",
    summary="Update a kanban stage",
    description="Update a kanban stage in the database",
    response_model=KanbanStageSchema
)
async def update_stage_endpoint(
    board_id: str,
    stage_id: str,
    title: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update a kanban stage in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update kanban stage in DB
    4. Return updated kanban stage
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_stage(board_id, stage_id, title)

# Route for deleting a kanban stage
@router.delete(
    "/stage",
    summary="Delete a kanban stage",
    description="Delete a kanban stage from the database"
)
async def delete_stage_endpoint(
    stage_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete a kanban stage from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete kanban stage from DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await delete_stage(stage_id)