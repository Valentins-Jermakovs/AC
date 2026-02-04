# Imports
from sqlmodel import (
    Session, 
    select, 
)
from ..models import (
    Role
)


'''
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
'''

# Initialize default system roles
def init_roles(engine):
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