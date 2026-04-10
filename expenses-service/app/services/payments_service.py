from app.models.payment_model import RecurringPayment
from datetime import datetime
from app.models.expense_model import Expense

# Create a new recurring payment
async def create_recurring(user_id: str, data):
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
async def get_recurring(user_id: str):
    return await RecurringPayment.find({
        "user_id": user_id
    }).to_list()


# Delete a recurring payment
async def delete_recurring(payment_id: str):
    payment = await RecurringPayment.get(payment_id)
    if payment:
        await payment.delete()


# Generate recurring expenses
async def generate_recurring_expenses():
    payments = await RecurringPayment.find_all().to_list()

    for p in payments:
        expense = Expense(
            user_id=p.user_id,
            amount=p.amount,
            category=p.category,
            date=datetime.now(),
            description="Auto-generated recurring payment"
        )

        await expense.insert()