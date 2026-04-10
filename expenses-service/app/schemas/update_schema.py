from pydantic import BaseModel
from datetime import date as DateType
from typing import Optional

class ExpenseUpdateSchema(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[DateType] = None
    description: Optional[str] = None