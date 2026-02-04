# Imports
from sqlmodel import Field, SQLModel

# UserRole model
# This class represents a user-role relationship in the database
#
# Attributes:
# - user_id (int): The ID of the user associated with the role.
# - role_id (int): The ID of the role associated with the user.

class UserRole(SQLModel, table=True):
    __tablename__ = 'user_roles'

    user_id: int = Field(
        foreign_key="users.id", 
        primary_key=True
    )

    role_id: int = Field(
        foreign_key="roles.id", 
        primary_key=True
    )