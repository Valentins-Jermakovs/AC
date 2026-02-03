# Imports
from sqlmodel import (
    SQLModel, 
    Session, 
    select, 
    create_engine
)
import os
from dotenv import load_dotenv
from ..models.models import (
    Role, 
    UserRole, 
    User, 
    Token
)

# ===== Database initialization service =====
# This module is responsible for initializing the database schema
# and seeding required system data (such as default roles).
# It is intended to be executed during application startup.

# Dotenv file contents read
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


# DB table inicialization
async def init_db():

    """
    Initialize database tables based on SQLModel metadata.

    Behavior:
    - Creates all database tables defined in SQLModel metadata
    - Safe to run multiple times (tables are created only if missing)

    Input:
    - None

    Output:
    - None
    """
        
    SQLModel.metadata.create_all(engine)


# Role table initialization
async def init_roles():

    """
    Initialize default system roles.

    Behavior:
    - Checks whether roles already exist in the database
    - If roles exist, initialization is skipped
    - If no roles exist, creates predefined roles required by the system

    Default roles:
    - user  : Read-only access, can manage own data
    - admin : Full access, can manage all system data

    Input:
    - None

    Output:
    - None
    """

    with Session(engine) as session:

        roles = {
            "user": "user can register and login, use system in read-only mode and write only own data",
            "admin": "administrator can register and login, use system in read-write mode and write all data"
        }

        existing_roles = session.exec(select(Role)).all()

        # Skip initialization if roles exist
        if existing_roles:
            return

        # Create default roles
        for role_name, role_description in roles.items():
            role = Role(name=role_name, description=role_description)
            session.add(role)

        session.commit()
