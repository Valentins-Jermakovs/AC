# Imports
from fastapi import HTTPException
from sqlmodel import Session, select
from ..models.models import User, Role, UserRole

"""
===== Authorization service =====
This service is responsible for role-based access control (RBAC).
It validates whether the current user has administrator privileges.
The service is designed to be reusable across multiple routes that require admin-level access.

Check whether the current user has an administrator role.

Input:
- current_user_id (int): ID of the currently authenticated user
- db (Session): Active database session

Behavior:
- Queries the database to retrieve the user's role
- Validates that the user has the administrator role
- Raises HTTP 403 if the user is not an administrator

Output:
- None (execution continues if the user is authorized)

Exceptions:
- HTTPException(403): Raised when the user does not have admin privileges
"""

# Admin role check function
def admin_required(
    current_user_id: int,
    db: Session
    ):
    
    user_role = db.exec(
        select(UserRole)
        .join(User, User.id == UserRole.user_id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == current_user_id)
    ).first()

    if user_role.role_id != 2:
        raise HTTPException(status_code=403, detail="Forbidden")