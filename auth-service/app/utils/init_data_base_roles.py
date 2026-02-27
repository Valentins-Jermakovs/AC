# =========================
# Default roles initialization (ASYNC)
# =========================

# Imports
# Libraries
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
# Models
from ..models import RoleModel


"""
Initializes default system roles asynchronously.
"""


# =========================
# Initialize roles
# =========================
async def init_roles(engine):

    async with AsyncSession(engine) as session:

        roles = {
            "user": "User can register, login and manage only own data",
            "admin": "Administrator with full system access",
            "developer": "Developer with full system access",
            "manager": "Manager with full system access",
            "support": "Support staff with full system access",
            "content_manager": "Content manager with full system access",
        }

        # Same SQL — no scalars changes
        result = await session.exec(select(RoleModel))
        existing_roles = result.all()

        # If roles already exist → skip
        if existing_roles:
            return

        # Create default roles
        for role_name, role_description in roles.items():
            session.add(
                RoleModel(
                    name=role_name,
                    description=role_description
                )
            )

        await session.commit()