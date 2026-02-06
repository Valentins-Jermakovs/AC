# =========================
# Database dependency
# =========================

# Imports
from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv


# =========================
# Load environment variables
# =========================
load_dotenv()   # Read .env file
DATABASE_URL = os.getenv("DATABASE_URL")    # Get database URL
engine = create_engine(DATABASE_URL, echo=True) # Create database engine with logging enabled


# =========================
# Database session dependency
# =========================
def get_db():
    """
    Provide a SQLModel Session for FastAPI endpoints.

    Usage:
    - Use `Depends(get_db)` in endpoints to access DB session.
    - Session is automatically closed after request.

    Steps:
    1. Create a new session bound to the database engine.
    2. Yield the session to the endpoint.
    3. Ensure session is closed in the finally block.

    Notes:
    - DATABASE_URL must be set in the .env file.
    - For Docker setup, use the DB container name in DATABASE_URL (e.g., auth_postgres).
    """
    session = Session(engine)   # Create new session
    try:                        
        yield session           # Provide session to endpoint
    finally:                    
        session.close()         # Close session