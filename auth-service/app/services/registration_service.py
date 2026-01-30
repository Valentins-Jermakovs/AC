# ===== Importi =====
from sqlmodel import Session, select
from fastapi import HTTPException

from ..models.models import User, Role, UserRole

from ..schemas.registration_schema import RegistrationSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema

from .password_service import get_password_hash
from .token_servicce import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)

# ===== Lietotāju reģistrācijas funkcija =====
def register_user(
    data: RegistrationSchema,
    db: Session
) -> TokenWithRefreshSchema:

    data.username = data.username.lower()
    data.email = data.email.lower()

    # ===== Lietotāja pārbaude =====
    existing_user = db.exec(
        select(User).where(User.username == data.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    existing_email = db.exec(select(User).where(User.email == data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # ===== Jaunā lietotāja reģistrācija =====
    user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password)
    )

    db.add(user)        
    db.commit()         
    db.refresh(user)    

    # ===== Noklusējuma lomas pievienošana =====
    user_role = db.exec(
        select(Role).where(Role.name == "user")
    ).first()

    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()

    # ===== Tokenu ģenerācija =====
    access_token = create_access_token({
        "sub": str(user.id)
    })
    refresh_token = create_refresh_token()
    save_refresh_token(refresh_token, user.id, db)

    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )
