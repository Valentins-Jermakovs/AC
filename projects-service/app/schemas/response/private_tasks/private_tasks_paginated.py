# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .private_task import PrivateTaskSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMetaSchema(BaseModel):
    page: int           # Current page number
    limit: int          # Number of items per page
    totalPages: int    # Total number of pages
    totalItems: int    # Total number of results

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "limit": 10,
                "total_pages": 1,
                "total_items": 1
            }
        }
    }

# ============================
# PaginatedPrivateTasks schema
# ============================
class PaginatedPrivateTasksSchema(BaseModel):
    items: List[PrivateTaskSchema] = Field(default_factory=list)    # List of private tasks
    meta: PaginationMetaSchema                                      # Pagination metadata

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "taskId": "1",
                        "title": "Private task 1",
                        "description": "Private task description 1",
                        "userId": "1",
                        "workspaceId": "1"
                    }
                ],
                "meta": {
                    "page": 1,
                    "limit": 10,
                    "total_pages": 1,
                    "total_items": 1
                }
            }
        }
    }