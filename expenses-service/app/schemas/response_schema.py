from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ExpenseResponse(BaseModel):
    id: str
    amount: float
    category: str
    date: datetime
    description: Optional[str]