# Imports
from fastapi import Depends, APIRouter
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utils
from app.utils.check_access_token import check_access_token
# Schemas
# ===== response:
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema
# ===== data:
from app.schemas.data.workspace.members.workspace_project_members_get_schema import WorkspaceProjectMembersGetSchema
from app.schemas.data.workspace.members.workspace_project_member_add_schema import WorkspaceProjectMemberAddSchema
from app.schemas.data.workspace.members.workspace_project_member_update_schema import WorkspaceProjectMemberUpdateSchema
from app.schemas.data.workspace.members.workspace_project_delete_member import WorkspaceProjectMemberDeleteSchema
# Services
from app.services.workspace.members.add_project_member_service import add_project_member
from app.services.workspace.members.get_all_members_service import get_all_project_members
from app.services.workspace.members.delete_member_service import delete_project_member
from app.services.workspace.members.update_project_member_role_service import update_project_member_role

# Router
router = APIRouter(
    prefix="/workspace/members",
    tags=["Workspace project member management service"]
)

# Security scheme for access token
security = HTTPBearer()

# ==== Project GET ==========================================================
# Route for getting all members of a project
@router.get(
    "/all",
)
async def get_all_project_members_endpoint(
    project_id: str, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    '''
    Get all members of a project

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to get all project members from DB
    4. Return all project members
    '''
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)
    
    return await get_all_project_members(
        projectId=project_id
    )

# ==== Project POST ==========================================================
# Route for adding a new member to a project
@router.post(
    "/add",
)
async def add_project_member_endpoint(
    data: WorkspaceProjectMemberAddSchema,
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

# ==== Project PUT ==========================================================
# Route for updating the role of a member in a project
@router.put(
    "/update-member",
    response_model=WorkspaceProjectMemberSchema
)
async def update_project_member_role_endpoint(
    data: WorkspaceProjectMemberUpdateSchema, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    '''
    Update the role of a member in a project

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to update project member role in DB
    '''
    
    access_token = credantials.credentials
    user_id_from_token = await check_access_token(access_token)
    
    return await update_project_member_role(
        projectId=data.project_id,
        userId=data.user_id,
        role=data.role
    )

# ==== Project DELETE ==========================================================
# Route for deleting a member from a project
@router.delete(
    "/delete",
)
async def delete_project_member_endpoint(
    data: WorkspaceProjectMemberDeleteSchema, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    
    access_token = credantials.credentials
    user_id_from_token = await check_access_token(access_token)
    
    return await delete_project_member(
        projectId=data.project_id,
        userId=data.user_id
    )





