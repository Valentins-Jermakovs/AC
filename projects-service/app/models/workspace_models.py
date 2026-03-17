# Imports
from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional
# Utilities
from app.utils.current_date import get_current_date

'''

Workspace models

- WorkspaceProjectModel: describe a workspace project
- WorkspaceStage: describe a workspace stage
- WorkspaceTask: describe a workspace task

Models are used to define the structure of the data stored in the database, 
and can be used to validate the data before it is saved.
'''

# ============================
# WorkspaceProject Model
# ============================
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


# ========================
# WorkspaceStage model
# ========================
class WorkspaceStageModel(Document):
    projectId: str  # Foreign key
    title: str      # Stage title
    order: int      # Stage order
    description: Optional[str] = None   # Stage description
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date
    dueDate: Optional[datetime] = None

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


# ========================
# WorkspaceTask model
# ========================
class WorkspaceTaskModel(Document):
    projectId: str                      # Project ID
    stageId: str                        # Stage ID
    title: str                          # Task title
    description: Optional[str] = None   # Optional description
    storyPoints: Optional[int] = None   # Optional story points
    priority: Optional[int] = None      # Optional priority
    status: Optional[str] = None        # Optional status
    order: float                        # Task order
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date
    dueDate: Optional[datetime] = None

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


# ============================
# WorkspaceProjectMember Model
# ============================
class WorkspaceProjectMemberModel(Document):
    email: str      # User email
    projectId: str  # Project ID
    userId: str     # User ID
    role: str       # Role

    class Settings:
        name = "workspace_project_members"
        indexes = [
            "projectId",    # Index for project ID
            "userId",       # Index for user ID
            [
                ("projectId", 1),   # Compound index for project ID
                ("userId", 1),      # and user ID
                ("role", 1)         # and role
            ],
        ]

