from app.models.payment_model import RecurringPayment
from app.models.expense_model import Expense
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

# Convert recurring payment to response
def to_response(payment: RecurringPayment):
    return {
        "id": str(payment.id),
        "amount": payment.amount,
        "category": payment.category,
        "start_date": payment.start_date,
        "interval": payment.interval
    }

# Create a new recurring payment
async def create_recurring(user_id: str, data):

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
async def get_recurring(user_id: str):

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
):
    payment = await RecurringPayment.get(payment_id)

    if not payment or payment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Recurring payment not found")

    await payment.delete()

    return {"message": "Recurring payment deleted successfully"}


# Update a recurring payment
async def update_recurring(
    payment_id: str,
    user_id: str,
    data
):
    payment = await RecurringPayment.get(payment_id)

    if not payment or payment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Recurring payment not found")

    update_data = data.model_dump(exclude_unset=True)

    payment = payment.model_copy(update=update_data)

    await payment.save()

    return to_response(payment)
