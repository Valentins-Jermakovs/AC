# =========================
# Database initialization
# =========================

# SQLModel core imports
from sqlmodel import (SQLModel, create_engine)
# Import all models so they are registered in metadata
from ..models import (
    Role,
    Token,
    User,
    UserRole
)
# Default roles initialization
from ..utils.init_data_base_roles import init_roles
# Environment variables
from dotenv import load_dotenv
import os

"""
Database tables initialization.

Behavior:
- Creates all database tables defined in SQLModel metadata
- Safe to run multiple times (tables are created only if missing)
- Initializes default system roles after tables are created

This function should be executed once on application startup.

Input:
- None

Output:
- None
"""


# =========================
# Database engine setup
# =========================

# Load environment variables from .env file
load_dotenv()
# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
# Create database engine
# echo=True enables SQL logging (useful for development)
engine = create_engine(
    DATABASE_URL, 
    echo=True
)


# =========================
# Initialize database
# =========================
def init_db():
    """
    Initializes database schema and default data.
    """

    # Create all tables if they do not exist
    SQLModel.metadata.create_all(engine)

    # Initialize default roles
    init_roles(engine)