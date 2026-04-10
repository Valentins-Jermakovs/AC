from datetime import date
from beanie import Document

class RecurringPayment(Document):
    user_id: str

    amount: float
    category: str

    start_date: date
    interval: str  # "monthly"

    class Settings:
        name = "recurring_payments"