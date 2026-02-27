# =========================
# Google OAuth authentication service (ASYNC)
# =========================

# Imports
# Libraries
from fastapi import Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
# Services
from ..tokens_management.create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)
# Models
from ...models import (
    UserRoleModel, 
    TokenModel, 
    UserModel
)
# Schemas
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema


async def google_auth_callback(
    oauth: OAuth,
    db: AsyncSession,
    request: Request
) -> TokenRefreshSchema:

    # -------------------------
    # 1. Get token from Google
    # -------------------------
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]
    google_id = user_info["sub"]

    # -------------------------
    # 2. Find user by google_id
    # -------------------------
    result = await db.exec(
        select(UserModel).where(UserModel.google_id == google_id)
    )
    user = result.first()  #  User object

    if user and not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # -------------------------
    # 3. If not found → search by email
    # -------------------------
    if not user:
        result = await db.exec(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.first()

        if user and not user.active:
            raise HTTPException(status_code=401, detail="User is inactive")

    # -------------------------
    # 4. Create or update user
    # -------------------------
    if user:
        user.google_id = google_id
        user.auth_provider = "google"
    else:
        user = UserModel(
            email=email,
            google_id=google_id,
            auth_provider="google",
            username=None,
            password_hash=None,
            active=True,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Assign default role
        db.add(UserRoleModel(user_id=user.id, role_id=1))
        await db.commit()

    # If user was updated (not new), commit changes
    await db.commit()
    await db.refresh(user)

    # -------------------------
    # 5. Delete old tokens
    # -------------------------
    result = await db.exec(
        select(TokenModel).where(TokenModel.user_id == user.id)
    )
    old_tokens = result.all()

    for t in old_tokens:
        await db.delete(t)

    await db.commit()

    # -------------------------
    # 6. Generate new tokens
    # -------------------------
    refresh_token_value = await create_refresh_token()
    await save_refresh_token(refresh_token_value, user.id, db)

    access_token = await create_access_token({"sub": str(user.id)})

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )