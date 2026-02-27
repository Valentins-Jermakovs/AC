# =========================
# User registration service (ASYNC)
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
# Models
from ...models import UserModel, RoleModel, UserRoleModel
# Schemas
from ...schemas.auth.registration_schema import RegistrationSchema
from ...schemas.tokens.token_refresh_schema import TokenRefreshSchema
# Password hashing
from ..passwords.passwords_service import get_password_hash
# Tokens
from ..tokens_management.create_tokens_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)


# =========================
# Register new user
# =========================
async def register_user(
    data: RegistrationSchema,
    db: AsyncSession
) -> TokenRefreshSchema:

    # Normalize
    data.username = data.username.lower()
    data.email = data.email.lower()

    # =========================
    # Check if username exists
    # =========================
    result = await db.exec(
        select(UserModel).where(UserModel.username == data.username)
    )
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # =========================
    # Check if email exists
    # =========================
    result = await db.exec(
        select(UserModel).where(UserModel.email == data.email)
    )
    existing_email = result.first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # =========================
    # Create user
    # =========================
    user = UserModel(
        username=data.username,
        email=data.email,
        password_hash= await get_password_hash(data.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # =========================
    # Assign default role
    # =========================
    result = await db.exec(
        select(RoleModel).where(RoleModel.name == "user")
    )
    user_role = result.first()

    if user_role:
        db.add(
            UserRoleModel(
                user_id=user.id,
                role_id=user_role.id
            )
        )
        await db.commit()

    # =========================
    # Generate tokens
    # =========================
    access_token = await create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token()

    await save_refresh_token(refresh_token, user.id, db)

    return TokenRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )