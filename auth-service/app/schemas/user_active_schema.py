# Šī shēma galvenokārt parāda vai lietotājs ir aktīvs
from pydantic import BaseModel

class UserActiveSchema(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool