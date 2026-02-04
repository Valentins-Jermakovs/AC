# Imports
from sqlmodel import (SQLModel, create_engine)
from ..models import (
    Role,
    Token,
    User,
    UserRole
)
from ..utils.init_data_base_roles import init_roles
from dotenv import load_dotenv
import os

'''
DB tables inicialization

Behavior:
- Creates all database tables defined in SQLModel metadata
- Safe to run multiple times (tables are created only if missing)

Input:
- None

Output:
- None
'''

# dotenv file contents read
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# DB tables inicialization
def init_db():
    SQLModel.metadata.create_all(engine)
    init_roles(engine)