# =========================
# Database dependency (ASYNC VERSION)
# =========================

# Imports - libraries
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


# =========================
# Load environment variables
# =========================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# =========================
# Database session dependency
# =========================
async def get_db():
    """
    Async database session dependency for FastAPI.
    Use with: Depends(get_db)
    """
    async with async_session() as session:
        yield session