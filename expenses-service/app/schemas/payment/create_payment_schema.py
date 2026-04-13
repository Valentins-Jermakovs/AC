from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class Interval(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class RecurringPaymentCreateSchema(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=3, max_length=100)
    start_date: date
    interval: Interval