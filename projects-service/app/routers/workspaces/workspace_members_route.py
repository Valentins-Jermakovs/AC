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
from app.services.workspace.members.get_member_by_email_service import get_member_by_email
from app.services.workspace.members.get_members_by_role_service import get_members_by_role
from app.services.workspace.members.get_current_user_service import get_current_user


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
    "/get-all-members",
)
async def get_all_project_members_endpoint(
    project_id: str,
    limit: int = 10,
    page: int = 1, 
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
        project_id=project_id,
        user_id=user_id,
        page=page,
        limit=limit
    )


# Get member by email
@router.get(
    "/get-member-by-email",
)
async def get_member_by_email_endpoint(
    email: str,
    project_id: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_member_by_email(
        email=email,
        project_id=project_id,
        page=page,
        limit=limit
    )

# Get members by role
@router.get(
    "/get-members-by-role",
)
async def get_members_by_role_endpoint(
    role: str,
    project_id: str,
    page: int = 1,
    limit: int = 10,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_members_by_role(
        role=role,
        project_id=project_id,
        page=page,
        limit=limit
    )

# Get current user
@router.get(
    "/get-current-user",
    response_model=WorkspaceProjectMemberSchema
)
async def get_current_user_endpoint(
    project_id: str,
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    return await get_current_user(
        project_id=project_id,
        user_id=user_id
    )

# ==== Project POST ==========================================================
# Route for adding a new member to a project
@router.post(
    "/add-member",
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
        email=data.email,
        project_id=data.projectId,
        user_id=data.userId,
        role=data.role,
        user_id_creator=user_id,
        mode="add"
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
        project_id=data.projectId,
        user_id=data.userId,
        role=data.role,
        user_id_creator=user_id_from_token
    )

# ==== Project DELETE ==========================================================
# Route for deleting a member from a project
@router.delete(
    "/delete-member",
)
async def delete_project_member_endpoint(
    data: WorkspaceProjectMemberDeleteSchema, 
    credantials: HTTPAuthorizationCredentials = Depends(security)
):
    '''
    Delete a member from a project

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to delete project member from DB
    '''
    
    access_token = credantials.credentials
    user_id_from_token = await check_access_token(access_token)
    
    return await delete_project_member(
        project_id=data.projectId,
        user_id=data.userId,
        user_id_requester=user_id_from_token
    )





