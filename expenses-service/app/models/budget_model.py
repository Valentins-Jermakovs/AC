from beanie import Document

class Budget(Document):
    user_id: str
    month: str  # "2026-04"
    category: str
    planned_amount: float

    class Settings:
        name = "budgets"