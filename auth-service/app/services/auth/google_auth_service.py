# Imports
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from fastapi import HTTPException
from urllib.parse import urljoin
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema
from ..tokens_management.create_tokens_service import (
    create_access_token, 
    create_refresh_token, 
    save_refresh_token
)
from ...models import (
    UserRole, 
    Token, 
    User
)

# The function `get_google_auth` is an asynchronous function that returns an HTTP response.`.
# After getting the redirect URI, it calls the `authorize_redirect` method of the `google` client in the `oauth` object.
async def get_google_auth(oauth: OAuth, request: Request):
    redirect_uri = urljoin(str(request.base_url), "auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# The function `google_auth_callback` is an asynchronous function that handles the callback from Google's authentication process.
async def google_auth_callback(oauth: OAuth, db: Session, request: Request) -> TokenRefreshSchema:

    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    email = user_info["email"]
    google_id = user_info["sub"]

    # try to find user by google_id
    user = db.exec(select(User).where(User.google_id == google_id)).first()
    if user and not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # if not found, try to find user by email
    if not user:
        user = db.exec(select(User).where(User.email == email)).first()

    if user:
        user.google_id = google_id
        user.auth_provider = "google"

    # if not found, create new user
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


    # Delete old tokens
    old_tokens = db.exec(select(Token).where(Token.user_id == user.id)).all()
    for t in old_tokens:
        db.delete(t)
    db.commit()

    # Generate new tokens
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)
    access_token = create_access_token({"sub": str(user.id)})

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )