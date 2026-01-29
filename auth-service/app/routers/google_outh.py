from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from urllib.parse import urljoin
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

from ..models.models import User, UserRole
from ..services.token_servicce import create_access_token
from ..services.base_connection import engine

load_dotenv()

router = APIRouter(prefix="/google", tags=["Google"])

# === DB dependency ===
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# === OAuth ===
oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile",
    },
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = urljoin(str(request.base_url), "auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]
    google_id = user_info["sub"]

    # meklē pēc google_id
    user = db.exec(
        select(User).where(User.google_id == google_id)
    ).first()

    # ja nav, pēc email
    if not user:
        user = db.exec(
            select(User).where(User.email == email)
        ).first()

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

        # pievieno lietotāja lomu
        db.add(UserRole(user_id=user.id, role_id=1))
        db.commit()
        db.refresh(user)


    # JWT
    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
