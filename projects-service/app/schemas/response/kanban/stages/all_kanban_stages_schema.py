# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from app.schemas.response.kanban.stages.kanban_stage_schema import KanbanStageSchema

# ================================
# AllKanbanStages schema - response
# ================================

class AllKanbanStagesSchema(BaseModel):
    items: List[KanbanStageSchema] = Field(default_factory=list)