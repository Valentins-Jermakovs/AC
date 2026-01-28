# === Serviss lietotāju autentifikācijai ===
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User
from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from ..services.password_service import verify_password
from ..services.token_servicce import create_access_token, create_refresh_token, save_refresh_token

# === lietotāju autentifikāciajs funkcija ===
def login_user(db: Session, data: LoginSchema) -> TokenWithRefreshSchema:

    # === pārbaudes uz esošu lietotāju ===
    user = db.exec(
        select(User).where(User.username == data.username)
    ).first()
    # === ja lietotājs neeksistē - 401 status kods ===
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # paroles salīdzināšana
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # === access tokena ģenerāciuja ===
    access_token = create_access_token({"sub": str(user.id),})
    # === refresh tokena ģenerācija ===
    refresh_token = create_refresh_token()
    # === saglabā refresh tokenu DB ===
    save_refresh_token(refresh_token, user.id, db)

    # atgriež tokenu un refresh tokenu
    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )
