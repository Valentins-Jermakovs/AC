# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== response:
from app.schemas.response.kanban.members.kanban_board_member_schema import KanbanBoardMemberSchema
from app.schemas.response.kanban.members.kanban_board_members_paginated_schema import KanbanBoardMembersPaginatedSchema
# ===== data:
from app.schemas.data.kanban.members.add_member_schema import AddMemberSchema
from app.schemas.data.kanban.members.update_member_schema import UpdateKanbanBoardMemberSchema
from app.schemas.data.kanban.members.remove_member_schema import RemoveKanbanBoardMemberSchema
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.kanban.members.add_board_member_service import add_board_member
from app.services.kanban.members.delete_board_member_service import delete_board_member
from app.services.kanban.members.get_all_members_service import get_all_members
from app.services.kanban.members.update_board_member_service import update_board_member

# Router
router = APIRouter(
    prefix="/kanban/members",
    tags=["Kanban board member management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== Kanban board member GET ==========================================================
# Route for getting all members of a kanban board
@router.get(
    "/get-all-members",
    response_model=KanbanBoardMembersPaginatedSchema
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

    return await get_all_members(
        board_id=board_id, 
        page=page, 
        limit=limit,
        user_id=user_id
    )

# ===== Kanban board member POST ==========================================================
# Route for adding a new member to a kanban board
@router.post(
    "/add-member",
    response_model=KanbanBoardMemberSchema
)
async def add_kanban_board_member_endpoint(
    data: AddMemberSchema,
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

    return await add_board_member(
        board_id=data.boardId, 
        user_id=data.userId,
        user_id_creator=user_id,
        mode="add",
        role=data.role
    )

# ===== Kanban board member PUT ==========================================================
# Route for updating a member of a kanban board
@router.put(
    "/update-member"
)
async def update_kanban_board_member_endpoint(
    data: UpdateKanbanBoardMemberSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update a member of a kanban board in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update board member in DB
    4. Return message
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_board_member(
        board_id=data.boardId,
        user_id=data.userId, 
        role=data.role
    )

# ===== Kanban board member DELETE ==========================================================
# Route for deleting a member from a kanban board
@router.delete(
    "/delete-member",
)
async def delete_kanban_board_member_endpoint(
    data: RemoveKanbanBoardMemberSchema,
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

    return await delete_board_member(
        user_id=data.userId, 
        board_id=data.boardId
    )