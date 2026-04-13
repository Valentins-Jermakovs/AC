from app.models.payment_model import RecurringPayment

# Create a new recurring payment
async def create_recurring(
    user_id: str, 
    data
):
    payment = RecurringPayment(
        user_id=user_id,
        amount=data.amount,
        category=data.category,
        start_date=data.start_date,
        interval=data.interval
    )

    await payment.save()
    return payment


# Get all recurring payments
async def get_recurring(
    user_id: str
):
    return await RecurringPayment.find({
        "user_id": user_id
    }).to_list()


# Delete a recurring payment
async def delete_recurring(
    payment_id: str
):
    payment = await RecurringPayment.get(payment_id)
    if payment:
        await payment.delete()


# Update a recurring payment
async def update_recurring(
    payment_id: str, 
    data
):
    payment = await RecurringPayment.get(payment_id)

    if not payment:
        return None

    update_data = data.model_dump(exclude_unset=True)

    payment = payment.model_copy(update=update_data)

    await payment.save()
    return payment