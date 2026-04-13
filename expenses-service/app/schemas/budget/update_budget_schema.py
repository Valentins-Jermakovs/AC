from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class BudgetUpdateSchema(BaseModel):
    month: Optional[str] = None
    category: Optional[str] = Field(None, min_length=3, max_length=100)
    planned_amount: Optional[float] = Field(None, gt=0)