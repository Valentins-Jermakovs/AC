# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
# Utils
from app.utils.check_access_token import check_access_token
# Schemas
# ===== response:
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema
from app.schemas.response.workspaces.projects.worskpace_projects_paginated_schema import WorkspaceProjectsPaginatedSchema
# ===== data:
from app.schemas.data.workspace.projects.workspace_project_update_schema import WorkspaceProjectUpdateSchema
from app.schemas.data.workspace.projects.workspace_project_create_schema import WorkspaceProjectCreateSchema
from app.schemas.data.workspace.projects.workspace_project_delete_schema import WorkspaceProjectDeleteSchema
from app.schemas.data.workspace.projects.workspace_project_title_or_description import WorkspaceProjectTitleOrDescription
# Services
from app.services.workspace.projects.create_project_service import create_project
from app.services.workspace.projects.update_project_service import update_project
from app.services.workspace.projects.delete_project_service import delete_project
from app.services.workspace.projects.get_all_projects_service import get_all_projects
from app.services.workspace.projects.get_project_by_title_service import get_project_by_title
# Router
router = APIRouter(
    prefix="/workspace/projects",
    tags=["Workspace project management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ==== Project GET ==========================================================
# Route for getting all projects
@router.get(
    "/get-all-projects",
    response_model=WorkspaceProjectsPaginatedSchema
)
async def get_all_projects_endpoint(
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all projects from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all projects from DB
    4. Return all projects
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_all_projects(
        user_id=user_id,
        page=page,
        limit=limit
    )


# Route for getting a project by title or description
@router.get(
    "/get-project-by-title",
    response_model=WorkspaceProjectsPaginatedSchema
)
async def get_project_by_title_endpoint(
    page: int = 1,
    limit: int = 10,
    title: Optional[str] = None,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get a project by title or description from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get project by title or description from DB
    4. Return project
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_project_by_title(
        title=title,
        limit=limit,
        page=page,
        user_id=user_id
    )

# ==== Project POST ==========================================================
# Route for creating a new project
@router.post(
    "/create-project",
    response_model=WorkspaceProjectSchema
)
async def create_project_endpoint(
    data: WorkspaceProjectCreateSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new project in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create project in DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await create_project(
        title=data.title,
        email=data.email,
        description=data.description, 
        user_id=user_id
    )

# ==== Project PUT ===========================================================
# Route for updating a project
@router.put(
    "/update-project",
    response_model=WorkspaceProjectSchema
)
async def update_project_endpoint(
    data: WorkspaceProjectUpdateSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update a project in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update project in DB
    4. Return updated project
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await update_project(
        user_id=user_id,
        project_id=data.projectId, 
        title=data.title, 
        description=data.description
    )

# ===== Project DELETE =======================================================
# Route for deleting a project
@router.delete(
    "/delete-project",
)
async def delete_project_endpoint(
    data: WorkspaceProjectDeleteSchema, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete a project from the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete project from DB
    4. Return deleted project
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await delete_project(
        project_id=data.projectId,
        user_id=user_id
    )