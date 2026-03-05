# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from app.schemas.response.workspaces.projects.workspace_project import WorkspaceProjectSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMetaSchema(BaseModel):
    page: int
    limit: int
    totalPages: int
    totalItems: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "limit": 10,
                "totalPages": 1,
                "totalItems": 1
            }
        }
    }

# ============================
# WorkspaceProjectsPaginatedSchema
# ============================
class WorkspaceProjectsPaginatedSchema(BaseModel):
    items: List[WorkspaceProjectSchema] = Field(default_factory=list)
    meta: PaginationMetaSchema

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "projectId": "1",
                        "title": "Project 1",
                        "description": "Project description 1",
                        "userId": "1",
                        "workspaceId": "1"
                    }
                ],
                "meta": {
                    "page": 1,
                    "limit": 10,
                    "totalPages": 1,
                    "totalItems": 1
                }
            }
        }
    }