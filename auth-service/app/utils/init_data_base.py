# =========================
# Database initialization (ASYNC)
# =========================

# Imports
# Libraries
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os
# Import models so metadata registers them
from ..models import RoleModel, TokenModel, UserModel, UserRoleModel
# Default roles
from ..utils.init_data_base_roles import init_roles


# =========================
# Load environment variables
# =========================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# =========================
# Async engine
# =========================
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# =========================
# Initialize database
# =========================
async def init_db():
    """
    Creates tables asynchronously and initializes default data.
    """

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Initialize roles AFTER tables are created
    await init_roles(engine)