from typing import Optional
from datetime import date
from pydantic import BaseModel


class ExpenseFilter(BaseModel):
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    category: Optional[str] = None