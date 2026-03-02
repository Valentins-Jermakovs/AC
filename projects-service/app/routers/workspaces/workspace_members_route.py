# Imports
from fastapi import Depends, APIRouter, Body
from typing import Annotated, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from ..utils.check_access_token import check_access_token
# Schemas
from ..schemas.response.workspace_member import WorkspaceProjectMemberSchema
from ..schemas.data.workspace_project_member_add import WorkspaceProjectMemberAddSchema
# Services
from ..services.workspace.add_project_member import add_project_member
from ..services.workspace.delete_member import delete_project_member
from ..services.workspace.get_all_members import get_all_project_members
from ..services.workspace.update_project_member_role import update_project_member_role

# Router
router = APIRouter(
    prefix="/members",
    tags=["Workspace project member management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for adding a new member to a project
@router.post(
    "/add",
    summary="Add a new member to a project",
    description="Add a new member to a project in the database",
)
async def add_project_member_endpoint(
    data: Annotated[WorkspaceProjectMemberAddSchema, Body(example={
        "project_id": "project_id",
        "user_id": "user_id",
        "role": "role"
    })],
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Add a new member to a project in the database.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to add member to project in DB
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await add_project_member(
        projectId=data.project_id,
        userId=data.user_id,
        role=data.role
    )

# Route for getting all members of a project
@router.get(
    "/all",
    summary="Get all members of a project",
    description="Get all members of a project from the database",
)
async def get_all_project_members_endpoint(projectId: str, credantials: HTTPAuthorizationCredentials = Depends(security)):
    
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)
    
    return await get_all_project_members(projectId)

# Route for deleting a member from a project
@router.delete(
    "/delete/{project_id}/{user_id}",
    summary="Delete a member from a project",
    description="Delete a member from a project from the database",
)
async def delete_project_member_endpoint(project_id: str, user_id: str, credantials: HTTPAuthorizationCredentials = Depends(security)):
    
    access_token = credantials.credentials
    user_id_from_token = await check_access_token(access_token)
    
    return await delete_project_member(project_id, user_id)

# Route for updating the role of a member in a project
@router.put(
    "/update-member",
    summary="Update the role of a member in a project",
    description="Update the role of a member in a project in the database",
)
async def update_project_member_role_endpoint(project_id: str, user_id: str, role: str, credantials: HTTPAuthorizationCredentials = Depends(security)):
    
    access_token = credantials.credentials
    user_id_from_token = await check_access_token(access_token)
    
    return await update_project_member_role(project_id, user_id, role)