from pydantic import BaseModel, Field
from datetime import date as DateType
from typing import Optional

class ExpenseUpdateSchema(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=3, max_length=100)
    date: Optional[DateType] = None
    description: Optional[str] = Field(None, min_length=3, max_length=1000)