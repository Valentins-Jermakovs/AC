# Imports
from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv


"""
Database Dependency

Function: get_db
----------------
Provides a SQLModel Session for FastAPI endpoints using dependency injection.

Usage:
- Can be used in endpoints with `Depends(get_db)` to access the database session.
- Ensures the session is properly closed after the request is finished.

Process:
1. Creates a new SQLModel Session bound to the configured database engine.
2. Yields the session to the caller (FastAPI endpoint).
3. Ensures the session is closed in the `finally` block after the endpoint completes.

Environment:
- DATABASE_URL should be set in a .env file for database connection.
"""


# dotenv file contents read
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Database connection
def get_db():                   
    session = Session(engine)   
    try:                        
        yield session
    finally:                    
        session.close()

# If FastAPI server will work in Docker container, 
# in localhost set an DB container name,
# for example auth_postgres