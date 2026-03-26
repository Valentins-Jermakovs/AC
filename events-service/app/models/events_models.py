# Imports
from enum import Enum
from beanie import Document
from datetime import datetime, time
from pydantic import Field
from typing import Optional
# Utilities
from app.utils.current_date import get_current_date

'''
Events models

- EventModel: describe an event

Models are used to define the structure of the data stored in the database, 
and can be used to validate the data before it is saved.
'''

# ===========================
# Color Enum
# ===========================
class ColorEnum(str, Enum):
    primary = "primary"
    secondary = "secondary"
    success = "success"
    warning = "warning"
    error = "error"
    info = "info"
    neutral = "neutral"

# ===========================
# Status Enum
# ==========================
class StatusEnum(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

# ===========================
# Event Model
# ===========================
class EventModel(Document):
    title: str                                              # Title of event
    description: Optional[str] = None                       # Description of event
    creatorId: str                                          # Id of creator
    startDate: datetime                                     # Start date of event
    endDate: datetime                                       # End date of event
    startTime: Optional[str] = None                        # Start time of event
    endTime: Optional[str] = None                          # End time of event
    allDay: bool = False                                    # If event is all day
    color: ColorEnum = ColorEnum.primary                    # Color of event
    status: StatusEnum = StatusEnum.active                  # Status of event
    createdAt: datetime = Field(default_factory=get_current_date)  # Creation date

    class Settings:
        name = "events"
        indexes = [
            "creatorId",        # Index for creator ID
            [
                ("creatorId", 1),   # Compound index for creator ID
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]