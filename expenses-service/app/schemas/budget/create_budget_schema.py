from pydantic import BaseModel
from datetime import date


class BudgetCreateSchema(BaseModel):
    month: str
    category: str
    planned_amount: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "month": "2026-04",
                "category": "Groceries",
                "planned_amount": 100.0
            }
        }
    }