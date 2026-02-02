# ===== Importi =====
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import Token

# ===== Refresh tokena dzēšanas funkcija =====
def logout(db: Session, refresh_token: str):
    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    db.delete(token)
    db.commit()

    return {"message": "Logout successful"}