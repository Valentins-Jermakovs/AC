from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal


class RecurringPaymentUpdateSchema(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    start_date: Optional[date] = None
    interval: Optional[Literal["daily", "weekly", "monthly"]] = None