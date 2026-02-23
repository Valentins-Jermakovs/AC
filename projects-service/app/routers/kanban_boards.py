# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.kanban_board import KanbanBoardSchema
from ..schemas.data.kanban_board_create import KanbanBoardCreateSchema
from ..schemas.data.kanban_board_update import KanbanBoardUpdateSchema
from ..schemas.response.kanban_boards_paginated import KanbanBoardsPaginatedSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.kanban.create_board import create_board
from ..services.kanban.update_board import update_board
from ..services.kanban.remove_board import remove_board
from ..services.kanban.find_board import find_board_by_title
from ..services.kanban.get_all_boards import get_all_boards_paginated

# Router
router = APIRouter(
    prefix="/kanban",
    tags=["Kanban board management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new kanban board
@router.post(
    "/create-board",
    summary="Create a new kanban board",
    description="Create a new kanban board in the database",
    response_model=KanbanBoardSchema
)
async def create_kanban_board_endpoint(
    data: Annotated[KanbanBoardCreateSchema, Body(example={"title": "Kanban board title"})],
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

    return await create_board(data.title, user_id)

# Route fro find all kanban boards paginated
@router.get(
    "/all-boards",
    summary="Get all kanban boards",
    description="Get all kanban boards from the database",
    response_model=KanbanBoardsPaginatedSchema
)
async def get_all_boards_endpoint(
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all kanban boards from the database with pagination.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all kanban boards from DB
    4. Return all kanban boards
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    all_boards = await get_all_boards_paginated(page, limit, user_id)

    return all_boards

# Route for find kanban board by title
@router.get(
    "/find-board-by-title",
    summary="Find a kanban board",
    description="Find a kanban board in the database",
    response_model=KanbanBoardsPaginatedSchema
)
async def find_kanban_board_endpoint(
    title: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Find a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to find kanban board in DB
    4. Return found kanban board
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await find_board_by_title(title=title, page=page, limit=limit, user_id=user_id)



# Route for updating a kanban board
@router.put(
    "/update-board",
    summary="Update a kanban board",
    description="Update a kanban board in the database",
    response_model=KanbanBoardSchema
)
async def update_kanban_board_endpoint(
    data: Annotated[KanbanBoardUpdateSchema, Body(example={"board_id": "board_id", "title": "Kanban board title"})],
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

    return await update_board(data.board_id, data.title)

# Route for remove kanban board by _id
@router.delete(
    "/remove-board/{board_id}",
    summary="Remove a kanban board",
    description="Remove a kanban board from the database"
)
async def remove_kanban_board_endpoint(
    board_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Remove a kanban board from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to remove kanban board from DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await remove_board(board_id, user_id)
