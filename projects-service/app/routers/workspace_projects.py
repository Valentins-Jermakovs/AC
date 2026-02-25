# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from ..utils.check_access_token import check_access_token
# Schemas
from ..schemas.response.workspace_project import WorkspaceProjectSchema
from ..schemas.data.workspace_project_create import WorkspaceProjectCreateSchema
from ..schemas.data.workspace_project_update import WorkspaceProjectUpdateSchema
# Services
from ..services.workspace.create_project import create_project
from ..services.workspace.update_project import update_project
from ..services.workspace.delete_project import delete_project
from ..services.workspace.get_all_projects import get_all_projects
from ..services.workspace.get_project_by_title import get_project_by_title_or_description
# Router
router = APIRouter(
    prefix="/projects",
    tags=["Workspace project management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new project
@router.post(
    "/create",
    summary="Create a new project",
    description="Create a new project in the database",
    response_model=WorkspaceProjectSchema
)
async def create_project_endpoint(
    data: Annotated[WorkspaceProjectCreateSchema, Body(example={
        "title": "Project title",
        "description": "Project description"
    })],
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

    return await create_project(title=data.title, description=data.description, user_id=user_id)


# Route for updating a project
@router.put(
    "/update",
    summary="Update a project",
    description="Update a project in the database",
    response_model=WorkspaceProjectSchema
)
async def update_project_endpoint(
    data: Annotated[WorkspaceProjectUpdateSchema, Body(example={
        "project_id": "project_id",
        "title": "Project title",
        "description": "Project description"
    })],
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

    return await update_project(data.project_id, data.title, data.description)


# Route for deleting a project
@router.delete(
    "/delete/{project_id}",
    summary="Delete a project",
    description="Delete a project from the database",
)
async def delete_project_endpoint(
    project_id: str, 
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

    return await delete_project(project_id)

# Route for getting all projects
@router.get(
    "/all",
    summary="Get all projects",
    description="Get all projects from the database",
)
async def get_all_projects_endpoint(
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

    return await get_all_projects(user_id)


# Route for getting a project by title or description
@router.get(
    "/get/{title_or_description}",
    summary="Get a project by title or description",
    description="Get a project by title or description from the database",
)
async def get_project_by_title_or_description_endpoint(
    title: Optional[str] = None,
    description: Optional[str] = None,
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

    return await get_project_by_title_or_description(title, description)