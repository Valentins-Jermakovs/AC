# Imports
from enum import Enum
from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional
# Utilities
from app.utils.current_date import get_current_date

'''
News models

- NewsModel: describe a news

Models are used to define the structure of the data stored in the database, 
and can be used to validate the data before it is saved.
'''

# ===========================
# Satus Enum
# ===========================
class StatusEnum(str, Enum):
    draft = "draft"
    published = "published"


# ===========================
# News Model
# ===========================
class NewsModel(Document):
    title: str
    content: str
    coverImage: Optional[str]
    status: StatusEnum = StatusEnum.draft
    tags: Optional[list[str]] = Field(default_factory=list)
    createdAt: datetime = Field(default_factory=get_current_date)
    publishedAt: Optional[datetime] = None
    authorId: str
    authorEmail: str

    class Settings:
        name = "news"
        indexes = [
            # Index for status and title
            [
                ("status", 1),      # Compound index for status
                ("title", 1)        # and title
            ]
        ]
