from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class Interval(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class RecurringPaymentCreateSchema(BaseModel):
    amount: float = Field(..., gt=0)
    category: str
    start_date: date
    interval: Interval