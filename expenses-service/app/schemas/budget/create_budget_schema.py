from pydantic import BaseModel, Field
from datetime import date


class BudgetCreateSchema(BaseModel):
    month: str
    category: str = Field(min_length=3, max_length=100)
    planned_amount: float = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "month": "2026-04",
                "category": "Groceries",
                "planned_amount": 100.0
            }
        }
    }