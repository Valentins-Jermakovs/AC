# =========================
# Google OAuth authentication service
# =========================

from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from fastapi import HTTPException
from urllib.parse import urljoin
# Token management utilities
from ..tokens_management.create_tokens_service import (
    create_access_token, 
    create_refresh_token, 
    save_refresh_token
)
# Database models
from ...models import UserRole, Token, User
# Response schema
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema

# =========================
# Handle Google OAuth callback
# =========================
async def google_auth_callback(
    oauth: OAuth, 
    db: Session, 
    request: Request
) -> TokenRefreshSchema:
    """
    Handles OAuth callback from Google, authenticates user, and generates tokens.

    Steps:
    1. Get token from Google
    2. Extract user info (email, Google ID)
    3. Find user in DB by Google ID
       - If inactive -> raise 401
    4. If not found -> find by email
    5. If still not found -> create new user
    6. Delete old tokens
    7. Generate new access & refresh tokens
    8. Return TokenRefreshSchema
    """

    # Get token and user info from Google
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    email = user_info["email"]
    google_id = user_info["sub"]

    print(f"Google ID: {google_id}")
    print(f"Email: {email}")
    print(f"Token: {token}")
    print(f"User info: {user_info}")
    print(f"access token: {request}")

    # Try to find user by Google ID
    user = db.exec(select(User).where(User.google_id == google_id)).first()
    if user and not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # If not found by Google ID, try by email
    if not user:
        user = db.exec(select(User).where(User.email == email)).first()

    # Update existing user with Google info
    if user:
        user.google_id = google_id
        user.auth_provider = "google"

    # Create new user if not found
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

        # Assign default role (user role ID = 1)
        db.add(UserRole(user_id=user.id, role_id=1))
        db.commit()


    # Delete old tokens for this user
    old_tokens = db.exec(select(Token).where(Token.user_id == user.id)).all()
    for t in old_tokens:
        db.delete(t)
    db.commit()

    # Generate new tokens
    refresh_token_value = create_refresh_token()
    save_refresh_token(refresh_token_value, user.id, db)

    access_token = create_access_token({"sub": str(user.id)})

    print(f"Access token: {access_token}")
    print(f"Refresh token: {refresh_token_value}")

    # Return response schema
    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )