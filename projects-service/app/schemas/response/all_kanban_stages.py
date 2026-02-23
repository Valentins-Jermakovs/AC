# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .kanban_stage import KanbanStageSchema

# ================================
# AllKanbanStages schema - response
# ================================

class AllKanbanStagesSchema(BaseModel):
    items: List[KanbanStageSchema] = Field(default_factory=list)