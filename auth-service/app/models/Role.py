# Imports
from sqlmodel import Field, SQLModel

# Role model
# This class represents a role in the database
#
# Attributes:
# - id (int): The unique identifier for the role.
# - name (str): The name of the role.
# - description (str): The description of the role.

class Role(SQLModel, table=True):
    __tablename__ = 'roles'                                     

    id: int = Field(primary_key=True)
    name: str = Field(
        max_length=50, 
        unique=True, 
        index=True
    )

    description: str = Field(max_length=100)