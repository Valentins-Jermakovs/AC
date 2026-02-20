# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.kanban_board import KanbanBoardSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.kanban.create_board import create_board
from ..services.kanban.update_board import update_board

# Router
router = APIRouter(
    prefix="/kanban",
    tags=["Kanban board management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new kanban board
@router.post(
    "/create",
    summary="Create a new kanban board",
    description="Create a new kanban board in the database",
)
async def create_kanban_board_endpoint(
    title: Annotated[str, Body(example="Kanban board title")],
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a new kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create kanban board in DB
    4. Return new kanban board
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await create_board(title, user_id)

# Route for updating a kanban board
@router.put(
    "/update",
    summary="Update a kanban board",
    description="Update a kanban board in the database",
)
async def update_kanban_board_endpoint(
    board_id: Annotated[str, Body(example="Kanban board ID")],
    title: Annotated[str, Body(example="Kanban board title")],
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update kanban board in DB
    4. Return updated kanban board
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_board(board_id, title)