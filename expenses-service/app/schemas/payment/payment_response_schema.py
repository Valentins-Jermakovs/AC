from pydantic import BaseModel
from datetime import date

class RecurringPaymentResponse(BaseModel):
    id: str
    amount: float
    category: str
    start_date: date
    interval: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "payment_id",
                    "amount": 100.0,
                    "category": "Groceries",
                    "start_date": "2023-01-01",
                    "interval": "monthly"
                }
            ]
        }
    }