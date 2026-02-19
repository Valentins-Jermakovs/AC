# Imports
from beanie import Document

# ============================
# WorkspaceProjectMember Model
# ============================
class WorkspaceProjectMember(Document):
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