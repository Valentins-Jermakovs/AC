from pydantic import BaseModel

class ExpenseStatsResponse(BaseModel):
    category: str
    total: float