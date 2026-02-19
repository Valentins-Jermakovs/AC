# Imports
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Schemas
from ..schemas.response.private_task import PrivateTaskSchema
from ..schemas.data.private_task_create import PrivateTaskCreateSchema
# utils
from ..utils.check_access_token import check_access_token
from ..services.private_tasks.create_private_task import create_private_task
router = APIRouter(
    prefix="/tasks",
    tags=["Private tasks management service"]
)

# Security scheme for access token
security = HTTPBearer()

# Route for creating a new private task
@router.post(
    "/create",
    summary="Create a new private task",
    description="Get JSON data and create a new private task in the database",
    response_model=PrivateTaskSchema
)
async def create_private_task_endpoint(
    data: PrivateTaskCreateSchema,
    credantials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a new private task.

    Steps:
    1. Extract access token
    2. Verify token and get user ID
    3. Call service to create private task in DB
    4. Return created private task
    """
    access_token = credantials.credentials
    user_id = await check_access_token(access_token)

    new_private_task = await create_private_task(data, user_id)

    return new_private_task

