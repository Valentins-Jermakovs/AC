# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utilities
from app.utils.check_access_token import check_access_token
# Services
from app.services.budget_service import (
    create_budget,
    update_budget,
    delete_budget,
    get_budgets
)
# Schemas
from app.schemas.budget.create_budget_schema import BudgetCreateSchema
from app.schemas.budget.update_budget_schema import BudgetUpdateSchema
from app.schemas.budget.message_response_schema import MessageResponse
from app.schemas.budget.budget_response_schema import BudgetResponse

# =========================
# ROUTER SETUP
# =========================
router = APIRouter(
    prefix="/budget",
    tags=["Budget management service"]
)

# Authentication dependency using HTTP Bearer token
security = HTTPBearer()


# =========================
# ROUTES
# =========================

# Create a budget
@router.post(
    "/create",
    response_model=BudgetResponse
)
async def create_budget_route(
    budget: BudgetCreateSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a budget for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `create_budget` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_budget(
        user_id=user_id,
        data=budget
    )


# Get a budget
@router.get(
    "/get",
    response_model=list[BudgetResponse]
)
async def get_budgets_route(
    month: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get budgets for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `get_budgets` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_budgets(
        user_id=user_id,
        month=month
    )


# Update a budget
@router.put(
    "/update",
    response_model=BudgetResponse
)
async def update_budget_route(
    budget: BudgetUpdateSchema,
    budget_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update a budget for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `update_budget` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await update_budget(
        budget_id=budget_id,
        data=budget,
        user_id=user_id
    )


# Delete budget
@router.delete(
    "/delete",
    response_model=MessageResponse
)
async def delete_budget_route(
    budget_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Delete a budget for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `delete_budget` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await delete_budget(
        budget_id=budget_id,
        user_id=user_id
    )