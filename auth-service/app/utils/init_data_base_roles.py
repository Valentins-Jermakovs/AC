# =========================
# Default roles initialization
# =========================

# SQLModel imports
from sqlmodel import Session, select

# Database model
from ..models import Role

"""
Initializes default system roles.

Behavior:
- Checks if any roles already exist in the database
- If roles exist, initialization is skipped
- If no roles exist, creates predefined system roles

This function should be called once during application startup.

Default roles:
- user             : Basic user, can manage only own data
- admin            : Full system access
- developer        : Full system access (technical role)
- manager          : Full system access (business role)
- support          : Full system access (support operations)
- content_manager  : Full system access (content management)

Input:
- engine : SQLModel / SQLAlchemy engine instance

Output:
- None
"""

# =========================
# Initialize roles
# =========================
def init_roles(engine):
    # Open database session
    with Session(engine) as session:

        # Predefined system roles (name -> description)
        roles = {
            "user": "User can register, login and manage only own data",
            "admin": "Administrator with full system access",
            "developer": "Developer with full system access",
            "manager": "Manager with full system access",
            "support": "Support staff with full system access",
            "content_manager": "Content manager with full system access",
        }

        # Check if roles already exist
        existing_roles = session.exec(
            select(Role)
        ).all()

        # If roles exist, do not create duplicates
        if existing_roles:
            return

        # Create default roles
        for role_name, role_description in roles.items():
            role = Role(
                name=role_name, 
                description=role_description
            )
            session.add(role)

        # Save changes to database
        session.commit()