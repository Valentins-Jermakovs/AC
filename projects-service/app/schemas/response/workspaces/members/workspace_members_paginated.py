# Imports
from pydantic import BaseModel, Field
from typing import List
# Models
from app.schemas.response.workspaces.members.workspace_member import WorkspaceProjectMemberSchema

# ===============================
# PaginationMeta schema - meta
# ===============================
class PaginationMetaSchema(BaseModel):
    page: int
    limit: int
    totalPages: int
    totalItems: int

# ================================
# WorkspaceProjectMembers schema - response
# ================================
class WorkspaceProjectMembersPaginatedSchema(BaseModel):
    items: List[WorkspaceProjectMemberSchema] = Field(default_factory=list)
    meta: PaginationMetaSchema