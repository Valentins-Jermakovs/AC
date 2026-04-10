from beanie import Document
from datetime import datetime, date
from typing import Optional
from pydantic import Field

class Expense(Document):
    user_id: str
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "expenses"
        indexes = [
            "user_id",
            "date",
            "category",
            [
                ("user_id", 1),
                ("date", -1),
                ("category", 1)
            ]
        ]