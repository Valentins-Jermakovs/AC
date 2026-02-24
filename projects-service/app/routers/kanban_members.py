# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.kanban_board_member import KanbanBoardMemberSchema
# Utils
from ..utils.check_access_token import check_access_token
# Services
from ..services.kanban.add_board_member import add_board_member
from ..services.kanban.delete_board_member import delete_board_member
from ..services.kanban.get_all_members import get_all_members
from ..services.kanban.update_board_member import update_board_member

# Router
router = APIRouter(
    prefix="/kanban/members",
    tags=["Kanban board member management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for adding a new member to a kanban board
@router.post(
    "/add-member",
    summary="Add a new member to a kanban board",
    description="Add a new member to a kanban board in the database",
    response_model=KanbanBoardMemberSchema
)
async def add_kanban_board_member_endpoint(
    data: Annotated[KanbanBoardMemberSchema, 
        Body(example={
            "boardId": "board_id", 
            "userId": "user_id", 
            "role": "role"})],
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Add a new member to a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to add board member to DB
    4. Return new board member
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await add_board_member(data.boardId, data.userId, data.role)

# Route for deleting a member from a kanban board
@router.delete(
    "/delete-member",
    summary="Delete a member from a kanban board",
    description="Delete a member from a kanban board in the database",
)
async def delete_kanban_board_member_endpoint(
    user_id: str,
    board_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Delete a member from a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete board member from DB
    """
    access_token = credantials.credentials
    current_user_id = await check_access_token(access_token)

    return await delete_board_member(user_id=user_id, board_id=board_id)


# Route for getting all members of a kanban board
@router.get(
    "/get-all-members",
    summary="Get all members of a kanban board",
    description="Get all members of a kanban board in the database",
)
async def get_all_kanban_board_members_endpoint(
    board_id: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get all members of a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all board members from DB
    4. Return all board members
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_members(board_id, page, limit)

# Route for updating a member of a kanban board
@router.put(
    "/update-member",
    summary="Update a member of a kanban board",
    description="Update a member of a kanban board in the database",
)
async def update_kanban_board_member_endpoint(
    boardId: str,
    userId: str,
    role:str,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update a member of a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update board member in DB
    4. Return updated board member
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_board_member(boardId,userId, role)