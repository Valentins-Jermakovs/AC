# ===== Importi =====
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from ..dependencies.get_current_user import get_current_user, get_user_role
from ..dependencies.data_base_connection import get_db

from ..models.models import User, Role, UserRole

# ===== Lietotāju lomu pārbaude =====
def admin_required(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
    
    user_role = db.exec(
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == current_user.id)
    ).first()

    print("USER:", current_user.id)
    print("ROLE:", user_role)

    if user_role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return user_role