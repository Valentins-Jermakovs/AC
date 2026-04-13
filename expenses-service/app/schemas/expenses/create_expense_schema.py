from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ExpenseCreateSchema(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=3, max_length=100)
    date: date
    description: str = Field(min_length=3, max_length=1000)