from beanie import Document
from datetime import datetime, date
from pydantic import Field
from typing import Optional
from pydantic import BaseModel

# ================================================
# Session model: stores information about a single user session
# ================================================
class Session(BaseModel):
    start: datetime                 # session start time
    end: Optional[datetime] = None  # session end time (optional)
    duration: Optional[int] = 0     # session duration in seconds

    # Close the session and calculate its duration
    def close(self, end_time: datetime):
        self.end = end_time
        self.duration = int((self.end - self.start).total_seconds())

# ================================================
# UserDailyActivity document: stores all daily activity for a user
# ================================================
class UserDailyActivity(Document):
    user_id: str                     # ID of the user
    date: date                       # date of activity
    first_visit: datetime            # timestamp of first visit of the day
    last_visit: datetime             # timestamp of last visit of the day
    visit_count: int = 1             # number of visits
    total_seconds: int = 0           # total seconds spent
    sessions: list[Session] = Field(default_factory=list)  # list of all sessions

    class Settings:
        name = "userDailyActivity"   # collection name in the database