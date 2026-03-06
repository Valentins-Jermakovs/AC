# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
# ===== response:
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema
from app.schemas.response.kanban.stages.all_kanban_stages_schema import AllKanbanStagesSchema
# ===== data:
from app.schemas.data.kanban.stages.create_stage_schema import CreateKanbanStageSchema
from app.schemas.data.kanban.stages.create_stage_relative_schema import KanbanStageCreateRelativeSchema
from app.schemas.data.kanban.stages.move_stage_schema import MoveKanbanStageSchema
from app.schemas.data.kanban.stages.update_stage_schema import UpdateKanbanStageSchema
from app.schemas.data.kanban.stages.remove_stage import RemoveKanbanStage
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.kanban.stages.kanban_stage_create_service import create_stage
from app.services.kanban.stages.insert_stage_relative_service import insert_stage_relative
from app.services.kanban.stages.get_all_stages_service import get_all_stages
from app.services.kanban.stages.move_stage_service import move_stage
from app.services.kanban.stages.update_stage_service import update_stage
from app.services.kanban.stages.delete_stage_service import delete_stage

# Router
router = APIRouter(
    prefix="/kanban/stages",
    tags=["Kanban stage management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== Stage GET ==========================================================
# Route for getting all kanban stages
@router.get(
    "/get-all-stages",
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

    return await get_all_stages(
        board_id=board_id,
        user_id=user_id
    )

# ===== Stage POST ==========================================================
# Route for creating a new kanban stage
@router.post(
    "/create-stage",
    response_model=KanbanStageSchema
)
async def create_stage_endpoint(
    data: CreateKanbanStageSchema,
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

    return await create_stage(
        board_id=data.boardId, 
        title=data.title,
        user_id=user_id
    )

# Create a new kanban stage relative
@router.post(
    "/create-relative-stage",
    response_model=KanbanStageSchema
)
async def create_stage_relative_endpoint(
    data: KanbanStageCreateRelativeSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new kanban stage relative in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create a new kanban stage relative in DB
    4. Return created kanban stage
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await insert_stage_relative(
        board_id=data.boardId, 
        title=data.title, 
        reference_stage_id=data.referenceStageId, 
        position=data.position,
        user_id=user_id
    )

# ===== Stage PUT ==========================================================
# Route for move a kanban stage
@router.put(
    "/move-stage",
)
async def move_stage_endpoint(
    data: MoveKanbanStageSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Move a kanban stage in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to move kanban stage in DB
    4. Return moved kanban stage
    """

    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await move_stage(
        board_id=data.boardId, 
        stage_id=data.stageId, 
        direction=data.direction,
        user_id=user_id
    )

# Route for updating a kanban stage
@router.put(
    "/update-stage",
    response_model=KanbanStageSchema
)
async def update_stage_endpoint(
    data: UpdateKanbanStageSchema,
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

    return await update_stage(
        board_id=data.boardId, 
        stage_id=data.stageId, 
        title=data.title,
        user_id=user_id
    )

# ===== Stage DELETE ==========================================================
# Route for deleting a kanban stage
@router.delete(
    "/delete-stage",
)
async def delete_stage_endpoint(
    data: RemoveKanbanStage,
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

    return await delete_stage(
        stage_id=data.stageId,
        board_id=data.boardId,
        user_id=user_id
    )