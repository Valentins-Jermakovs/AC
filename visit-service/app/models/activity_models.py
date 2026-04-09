from beanie import Document
from datetime import datetime, date
from pydantic import Field
from typing import Optional
from pydantic import BaseModel

class Session(BaseModel):
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[int] = 0

    def close(self, end_time: datetime):
        self.end = end_time
        self.duration = int((self.end - self.start).total_seconds())


class UserDailyActivity(Document):

    user_id: str
    date: date
    first_visit: datetime
    last_visit: datetime
    visit_count: int = 1
    total_seconds: int = 0
    sessions: list[Session] = Field(default_factory=list)

    class Settings:
        name="userDailyActivity"