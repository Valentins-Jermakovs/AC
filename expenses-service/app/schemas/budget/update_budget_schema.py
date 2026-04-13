from pydantic import BaseModel
from datetime import date
from typing import Optional


class BudgetUpdateSchema(BaseModel):
    month: Optional[str] = None
    category: Optional[str] = None
    planned_amount: Optional[float] = None