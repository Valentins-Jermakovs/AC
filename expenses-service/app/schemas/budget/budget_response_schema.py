from pydantic import BaseModel

class BudgetResponse(BaseModel):
    id: str
    month: str
    category: str
    planned_amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "budget_id",
                    "month": "2023-04",
                    "category": "Groceries",
                    "planned_amount": 100.0
                }
            ]
        }
    }