# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Utilities
from app.utils.check_access_token import check_access_token
# Services
from app.services.payments_service import (
    create_recurring,
    update_recurring,
    delete_recurring,
    get_recurring,
)
# Schemas
from app.schemas.payment.create_payment_schema import RecurringPaymentCreateSchema
from app.schemas.payment.update_payment_schema import RecurringPaymentUpdateSchema
from app.schemas.payment.payment_response_schema import RecurringPaymentResponse
from app.schemas.payment.message_response import MessageResponse


# =========================
# ROUTER SETUP
# =========================
router = APIRouter(
    prefix="/payment",
    tags=["Payment management service"]
)

# Authentication dependency using HTTP Bearer token
security = HTTPBearer()


# =========================
# ROUTES
# =========================
# Create a recurring payment
@router.post(
    "/create",
    response_model=RecurringPaymentResponse
)
async def create_recurring_route(
    payment: RecurringPaymentCreateSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a recurring payment for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `create_recurring` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_recurring(
        user_id=user_id,
        data=payment
    )

# Get all recurring payments
@router.get(
    "/get",
    response_model=list[RecurringPaymentResponse]
)
async def get_recurring_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get recurring payments for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `get_recurring` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_recurring(
        user_id=user_id
    )


# update a recurring payment
@router.put(
    "/update/{payment_id}",
    response_model=RecurringPaymentResponse
)
async def update_recurring_route(
    payment_id: str,
    payment: RecurringPaymentUpdateSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Update a recurring payment for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `update_recurring` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await update_recurring(
        payment_id=payment_id,
        data=payment,
        user_id=user_id
    )

# delete a recurring payment
@router.delete(
    "/delete/{payment_id}",
    response_model=MessageResponse
)
async def delete_recurring_route(
    payment_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Delete a recurring payment for the current user.

    - Requires authentication
    - Validates user via access token
    - Uses `delete_recurring` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await delete_recurring(
        payment_id=payment_id,
        user_id=user_id
    )