# Imports
from pydantic import BaseModel

# ============================================================
# PrivateTaskRemove schema for removing a private task
# ============================================================
class PrivateTaskRemove(BaseModel):
    taskId: str # The ID of the task to remove