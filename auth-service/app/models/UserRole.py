# =========================
# UserRole model
# =========================

# Imports
from sqlmodel import Field, SQLModel  # SQLModel base and fields


# =========================
# UserRole table in database
# =========================
class UserRole(SQLModel, table=True):
    """
    Represents the relationship between users and roles in the database.

    Attributes:
    - user_id (int): ID of the user (foreign key to users table)
    - role_id (int): ID of the role (foreign key to roles table)
    
    Notes:
    - Composite primary key: (user_id, role_id)
    - Each row represents one role assigned to one user
    """
    __tablename__ = 'user_roles'

    user_id: int = Field(
        foreign_key="users.id",  # Reference to users table
        primary_key=True
    )

    role_id: int = Field(
        foreign_key="roles.id",  # Reference to roles table
        primary_key=True
    )
