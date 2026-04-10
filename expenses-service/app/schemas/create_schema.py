from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseCreateSchema(BaseModel):
    amount: float
    category: str
    date: date
    description: Optional[str] = None