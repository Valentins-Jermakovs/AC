# Imports
from typing import Optional
from datetime import datetime
from pydantic import Field
# Utilities
from ..utils.current_date import get_current_date

# ========================
# WorkspaceTask model
# ========================
class WorkspaceTask:
    projectId: str                      # Project ID
    stageId: str                        # Stage ID
    title: str                          # Task title
    description: Optional[str] = None   # Optional description
    storyPoints: Optional[int] = None   # Optional story points
    priority: Optional[int] = None      # Optional priority
    status: Optional[str] = None        # Optional status
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date

    class Settings:
        name = "workspace_tasks"
        indexes = [
            "projectId",        # Index for project ID
            "stageId",          # Index for stage ID
            [
                ("projectId", 1),   # Compound index for project ID
                ("stageId", 1),     # and stage ID
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]