# ===== Importi =====
from fastapi import Depends, HTTPException
from sqlmodel import Session
from ..dependencies.get_current_user import get_current_user, get_user_role
from ..dependencies.data_base_connection import get_db

from ..models.models import User

# ===== Lietotāju lomu pārbaude =====
def admin_required(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
    role = get_user_role(current_user.id, db)
    if role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user