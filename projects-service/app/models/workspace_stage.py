# Imports
from typing import Optional
from datetime import datetime
from pydantic import Field
from beanie import Document
# Utilities
from ..utils.current_date import get_current_date

# ========================
# WorkspaceStage model
# ========================
class WorkspaceStage(Document):
    projectId: str  # Foreign key
    title: str      # Stage title
    order: int      # Stage order
    description: Optional[str] = None   # Stage description
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date

    class Settings:
        name = "workspace_stages"
        indexes = [
            "projectId",        # Index for project ID
            "order",            # Index for order
            [
                ("projectId", 1),   # Compound index for project ID
                ("order", 1),       # and order
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]