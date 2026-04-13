
from pydantic import BaseModel
from datetime import date

class CategoryStat(BaseModel):
    category: str
    total: float

class TimelinePoint(BaseModel):
    date: date
    total: float

class ExpenseStats(BaseModel):
    total: float
    by_category: list[CategoryStat]