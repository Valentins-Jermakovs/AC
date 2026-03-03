# Imports
from pydantic import BaseModel
from typing import Optional

# ============================================================
# WorkspaceProjectTitleOrDescription schema for getting a workspace project by title or description
# ============================================================
class WorkspaceProjectTitleOrDescription(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    limit: Optional[int] = 10
    page: Optional[int] = 1

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Project title - optional",
                    "description": "Project description - optional",
                    "limit": 10,
                    "page": 1
                }
            ]
        }
    }