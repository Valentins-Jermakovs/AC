from app.models.payment_model import RecurringPayment
from fastapi import HTTPException
from app.schemas.payment.create_payment_schema import RecurringPaymentCreateSchema
from app.schemas.payment.update_payment_schema import RecurringPaymentUpdateSchema
from app.schemas.payment.payment_response_schema import RecurringPaymentResponse
from app.schemas.payment.message_response import MessageResponse
from bson import ObjectId

# Convert recurring payment to response
def to_response(
    payment: RecurringPayment
) -> RecurringPaymentResponse:
    return RecurringPaymentResponse(
        id=str(payment.id),
        amount=payment.amount,
        category=payment.category,
        start_date=payment.start_date,
        interval=payment.interval
    )

# Create a new recurring payment
async def create_recurring(
    user_id: str, 
    data: RecurringPaymentCreateSchema
) -> RecurringPaymentResponse:

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    payment = RecurringPayment(
        user_id=user_id,
        amount=data.amount,
        category=data.category,
        start_date=data.start_date,
        interval=data.interval
    )

    await payment.save()
    return to_response(payment)


# Get all recurring payments
async def get_recurring(
    user_id: str
) -> list[RecurringPaymentResponse]:

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    payments = await RecurringPayment.find({
        "user_id": user_id
    }).to_list()

    return [to_response(p) for p in payments]


# Delete a recurring payment
async def delete_recurring(
    payment_id: str,
    user_id: str
) -> MessageResponse:
    
    if ObjectId.is_valid(payment_id) is False:
        raise HTTPException(status_code=400, detail="Invalid payment ID")

    payment = await RecurringPayment.get(payment_id)

    if not payment or payment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Recurring payment not found")

    await payment.delete()

    return {"message": "Recurring payment deleted successfully"}


# Update a recurring payment
async def update_recurring(
    payment_id: str,
    user_id: str,
    data: RecurringPaymentUpdateSchema
) -> RecurringPaymentResponse:
    
    if ObjectId.is_valid(payment_id) is False:
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    
    payment = await RecurringPayment.get(payment_id)

    if not payment or payment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Recurring payment not found")

    update_data = data.model_dump(exclude_unset=True)

    payment = payment.model_copy(update=update_data)

    await payment.save()

    return to_response(payment)
