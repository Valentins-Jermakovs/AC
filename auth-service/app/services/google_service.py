# ===== Importi =====
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from fastapi import HTTPException
from urllib.parse import urljoin

from ..services.token_service import (
    create_access_token, 
    create_refresh_token, 
    save_refresh_token
)

from ..models.models import (
    UserRole, 
    Token, 
    User
)

async def get_google_auth(oauth: OAuth, request: Request):
    redirect_uri = urljoin(str(request.base_url), "auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def google_auth_callback(oauth: OAuth, db: Session, request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]
    google_id = user_info["sub"]

    # meklē pēc google_id
    user = db.exec(select(User).where(User.google_id == google_id)).first()
    if user and not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # ja nav, meklē pēc email
    if not user:
        user = db.exec(select(User).where(User.email == email)).first()

    if user:
        user.google_id = google_id
        user.auth_provider = "google"
    else:
        user = User(
            email=email,
            google_id=google_id,
            auth_provider="google",
            username=None,
            password_hash=None,
            active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.add(UserRole(user_id=user.id, role_id=1))
        db.commit()


    # ===== Dzēš visus vecos refresh tokenus =====
    old_tokens = db.exec(select(Token).where(Token.user_id == user.id)).all()
    for t in old_tokens:
        db.delete(t)
    db.commit()

    # ===== Ģenerē jauno refresh tokenu =====
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)

    # ===== JWT ģenerācija =====
    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
