# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from app.schemas.response.workspaces.stages.workspace_stage_schema import WorkspaceStageSchema

# ================================
# WorkspaceGetAllStages schema - response
# ================================
class WorkspaceGetAllStagesSchema(BaseModel):
    items: List[WorkspaceStageSchema] = Field(default_factory=list)

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "id": "17823gfdsabv213",
                        "title": "Stage 1",
                        "description": "Stage description 1",
                        "project_id": "1",
                        "order": 1000,
                        "due_date": "2026-01-01",
                        "created_at": "2022-01-01"
                    }
                ]
            }
        }
    }