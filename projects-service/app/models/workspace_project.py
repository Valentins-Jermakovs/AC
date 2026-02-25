# Imports
from datetime import datetime
from pydantic import Field
from typing import Optional
from beanie import Document
# Utilities
from ..utils.current_date import get_current_date

class WorkspaceProjectModel(Document):
    userId: str        # User ID (owner)
    title: str         # Project title
    description: Optional[str] = None                                # Project description
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date (auto-generated)

    class Settings:
        name = "workspace_projects"
        indexes = [
            "userId",       # Index for user ID
            "title",        # Index for title
            [
                ("userId", 1),      # Compound index for user ID
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]