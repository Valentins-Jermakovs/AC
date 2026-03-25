# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
# Utils
from app.utils.check_access_token import check_access_token
# Services
from app.services.workspace.selected_project.set_selected_project_service import set_selected_project_service
from app.services.workspace.selected_project.get_count_stages_selected_project_service import get_stages_count, get_stages_date_range
from app.services.workspace.selected_project.count_tasks_service_selected_project import get_project_tasks_stats
# Schemas
from app.schemas.data.selected_project.select_project_schema import SelectedProject

# Router
router = APIRouter(
    prefix="/workspace/selected-project",
    tags=["Workspace selected project management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for create or update selected project
@router.put(
    "/set-selected-project",
)
async def set_selected_project_endpoint(
    data: SelectedProject,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Set selected project in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to set selected project in DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await set_selected_project_service(
        userId=user_id,
        workspaceId=data.workspaceId,
        workspaceTitle=data.workspaceTitle
    )

# Route for getting count of selected project stages
@router.get(
    "/get-stages-count",
)
async def get_stages_count_endpoint(
    projectId: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get count of selected project stages from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get count of selected project stages from DB
    4. Return count of selected project stages
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_stages_count(
        user_id=user_id,
        project_id=projectId
    )

# Route for getting create date and due date of selected project stages
@router.get(
    "/get-stages-date-range",
)
async def get_stages_date_range_endpoint(
    projectId: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get create date and due date of selected project stages from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get create date and due date of selected project stages from DB
    4. Return create date and due date of selected project stages
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_stages_date_range(
        user_id=user_id,
        project_id=projectId
    )

# Route for count all tasks in project
@router.get(
    "/get-project-tasks-stats",
)
async def get_project_tasks_stats_endpoint(
    projectId: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get count of selected project stages from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get count of selected project stages from DB
    4. Return count of selected project stages
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_project_tasks_stats(
        user_id=user_id,
        project_id=projectId
    )