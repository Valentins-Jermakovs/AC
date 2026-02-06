# =========================
# Role model
# =========================

# Imports
from sqlmodel import Field, SQLModel


# =========================
# Role table in database
# =========================
class Role(SQLModel, table=True):
    """
    Represents a role in the database.

    Attributes:
    - id (int): Unique identifier for the role (primary key)
    - name (str): Role name, unique and indexed
    - description (str): Short description of the role
    """
    __tablename__ = 'roles'                                     

    id: int = Field(primary_key=True)   # Primary key
    name: str = Field(
        max_length=50, 
        unique=True,                    # No duplicate role names
        index=True                      # Indexed for faster lookups
    )

    description: str = Field(max_length=100)    # Role description