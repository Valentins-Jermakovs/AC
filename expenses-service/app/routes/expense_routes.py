# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utilities
from app.utils.check_access_token import check_access_token
# Services
from app.services.expense_service import (
    create_expense,
    update_expense,
    delete_expense,
    get_expenses,
    get_stats
)
# Schemas
from app.schemas.create_schema import ExpenseCreateSchema
from app.schemas.update_schema import ExpenseUpdateSchema
from app.schemas.response_schema import ExpenseResponse
from app.schemas.filters_schema import ExpenseFilter

# =========================
# ROUTER SETUP
# =========================
router = APIRouter(
    prefix="/expense",
    tags=["Expense management service"]
)

# Authentication dependency using HTTP Bearer token
security = HTTPBearer()

# =========================
# ROUTES
# =========================

# Create an expense
@router.post(
    "/create",
    response_model=ExpenseResponse,
)
async def create_expense_route(
    expense: ExpenseCreateSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create an expense for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `create_expense` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_expense(
        data=expense,
        user_id=user_id
    )



# Get expenses for the current user
@router.get(
    "/get",
    response_model=list[ExpenseResponse],
)
async def get_expenses_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    filters: ExpenseFilter = Depends()
):
    """
    Get expenses for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `get_expenses` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_expenses(
        user_id=user_id, 
        filters=filters
    )



# Get stats for the current user
@router.get(
    "/stats",
)
async def get_stats_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get stats for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `get_stats` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_stats(
        user_id=user_id
    )


# Update an expense
@router.put(
    "/update/{expense_id}",
    response_model=ExpenseResponse,
)
async def update_expense_route(
    expense_id: str,
    expense: ExpenseUpdateSchema,
):
    """
    Update an expense for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `update_expense` service
    """

    return await update_expense(
        expense_id=expense_id,
        data=expense
    )



# Delete an expense
@router.delete(
    "/delete/{expense_id}",
)
async def delete_expense_route(
    expense_id: str,
):
    """
    Delete an expense for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `delete_expense` service
    """

    return await delete_expense(
        expense_id=expense_id
    )