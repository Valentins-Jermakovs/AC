# Šī shēma galvenokārt parāda vai lietotājs ir aktīvs
from pydantic import BaseModel
from typing import Optional

class UserActiveSchema(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    is_active: bool