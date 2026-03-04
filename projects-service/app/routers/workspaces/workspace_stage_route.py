# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from app.utils.check_access_token import check_access_token
# Schemas
# ===== response:
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema
from app.schemas.response.workspaces.stages.workspace_stage_get_all_schema import WorkspaceGetAllStagesSchema as WorkspaceGetAllStagesResponse
# ===== data:
from app.schemas.data.workspace.stages.workspace_stage_create_schema import WorkspaceStageCreateSchema
from app.schemas.data.workspace.stages.workspace_stage_delete_schema import WorkspaceStageDelete
from app.schemas.data.workspace.stages.workspace_stage_update_schema import WorkspaceStageUpdateSchema
from app.schemas.data.workspace.stages.workspace_get_all_stages_schema import WorkspaceGetAllStagesSchema
from app.schemas.data.workspace.stages.workspace_move_stage_schema import WorkspaceMoveStageSchema
from app.schemas.data.workspace.stages.workspace_insert_stage_relative_schema import WorkspaceInsertStageRelativeSchema
# Services
from app.services.workspace.stages.workspace_stage_create_service import create_stage
from app.services.workspace.stages.worskpace_stage_delete_service import delete_stage
from app.services.workspace.stages.workspace_stage_update_service import update_stage
from app.services.workspace.stages.workspace_get_all_stages_service import get_all_stages
from app.services.workspace.stages.workspace_move_stage_service import move_stage
from app.services.workspace.stages.workspace_insert_stage_reative_service import insert_stage_relative
# Router
router = APIRouter(
    prefix="/workspace/stages",
    tags=["Workspace stage management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ===== Stage GET ==========================================================
# Route for getting all kanban stages
@router.get(
    "/all",
    response_model=WorkspaceGetAllStagesResponse
)
async def get_all_stages_endpoint(
    project_id: str,
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
        project_id=project_id
    )

# ===== Stage POST ==========================================================
# Route for creating a new project stage
@router.post(
    "/create",
    response_model=WorkspaceStageSchema
)
async def create_stage_endpoint(
    data: WorkspaceStageCreateSchema,
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
        title=data.title,
        description=data.description,
        project_id=data.project_id
    )

# Route for creating new stage relative to another stage
@router.post(
    "/insert-relative",
    response_model=WorkspaceStageSchema
)
async def insert_stage_relative_endpoint(
    data: WorkspaceInsertStageRelativeSchema,
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

    return await insert_stage_relative(
        project_id=data.project_id,
        title=data.title,
        reference_stage_id=data.reference_stage_id,
        position=data.position,
        description=data.description
    )

# ===== Stage PUT ==========================================================
# Route for updating a kanban stage
@router.put(
    "/update",
    response_model=WorkspaceStageSchema
)
async def update_stage_endpoint(
    data: WorkspaceStageUpdateSchema,
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
        stage_id=data.stage_id,
        title=data.title,
        description=data.description
    )

# Route for moving a kanban stage
@router.put(
    "/move"
)
async def move_stage_endpoint(
    data: WorkspaceMoveStageSchema,
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
        project_id=data.project_id, 
        stage_id=data.stage_id, 
        direction=data.direction
    )

# ===== Stage DELETE ==========================================================
# Route for deleting a kanban stage
@router.delete(
    "/delete",
)
async def delete_stage_endpoint(
    data: WorkspaceStageDelete,
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
        stage_id=data.stage_id
    )