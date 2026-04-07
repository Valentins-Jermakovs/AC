# =========================
# IMPORTS
# =========================
from enum import Enum
from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional

# Utilities
from app.utils.current_date import get_current_date

# =========================
# MODULE DESCRIPTION
# =========================
"""
News Models

- NewsModel: Represents a news item in the database

Purpose:
- Defines the structure of news data
- Validates data before saving to MongoDB
- Used by Beanie ODM to map Python objects to database documents
"""

# =========================
# STATUS ENUM
# =========================
class StatusEnum(str, Enum):
    """
    Status of a news item:
    - draft: not published yet
    - published: visible to users
    """
    draft = "draft"
    published = "published"


# =========================
# NEWS MODEL
# =========================
class NewsModel(Document):
    """
    Main News document model for MongoDB.
    
    Fields:
    - title: Title of the news
    - content: HTML content of the news
    - coverImage: Optional URL of the cover image
    - status: Draft or published
    - tags: List of tags (lowercased)
    - createdAt: Date when news was created
    - publishedAt: Date when news was published (if published)
    - authorId: ID of the author
    - authorEmail: Email of the author
    """

    title: str
    content: str
    coverImage: Optional[str] = None
    status: StatusEnum = StatusEnum.draft
    tags: Optional[list[str]] = Field(default_factory=list)
    createdAt: datetime = Field(default_factory=get_current_date)
    publishedAt: Optional[datetime] = None
    authorId: str
    authorEmail: str

    # =========================
    # BEANIE SETTINGS
    # =========================
    class Settings:
        # MongoDB collection name
        name = "news"

        # Indexes for faster queries
        indexes = [
            # Compound index: status + title
            [
                ("status", 1),  # 1 = ascending
                ("title", 1)
            ]
        ]