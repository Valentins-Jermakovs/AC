# Imports
from datetime import datetime
from typing import Optional
from fastapi import HTTPException

# =============================
# Converter to datetime format
# =============================
async def convert_to_datetime(dueDate: Optional[str]) -> Optional[datetime]:
    if dueDate:
        try:
            return datetime.fromisoformat(dueDate)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid date format. Use YYYY-MM-DD"
            )
    return None
