# ===== Importi =====
from sqlmodel import Session, select
from fastapi import HTTPException

from ..models.models import User, Token

from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema

from ..services.password_service import verify_password
from ..services.token_servicce import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


# ===== Lietotāju autentifikāciajs funkcija =====
def login_user(db: Session, data: LoginSchema) -> TokenWithRefreshSchema:

    data.username = data.username.lower()

    # ===== Lietotāja pārbaude =====

    user = db.exec(
        select(User).where(User.username == data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    if not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")


    # ===== Veco refresh tokenu dzēšana (rotation) =====
    token = db.exec(
        select(Token)
        .where(Token.user_id == user.id)
        .order_by(Token.created_at.desc())
    ).first()

    if token:
        db.delete(token)
        db.commit()


    # ===== Jauno tokenu ģenerācija =====
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)
    access_token = create_access_token({
        "sub": str(user.id)
    })

    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )
