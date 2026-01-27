from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, timezone, timedelta

def utcnow() -> datetime: # datuma un laika iestatīšanas funkcija
    return datetime.now(timezone.utc)

# lietotāja modelis
class User(SQLModel, table=True):
    __tablename__ = 'users'                                         # lietotāja tabula

    id: int = Field(default=None, primary_key=True)                 # lietotāja id
    username: str = Field(max_length=50, index=True, unique=True)   # lietotāja vards
    password_hash: str = Field(max_length=255)                      # lietotāja parole
    email: str = Field(max_length=100, index=True, unique=True)     # lietotāja e-pasts
    created_at: datetime = Field(default_factory=utcnow)            # lietotāja izveide datums
    active: bool = Field(default=True)                              # lietotāja statuss

# lomas modelis
class Role(SQLModel, table=True):
    __tablename__ = 'roles'                                     # lietotāju lomu tabula

    id: int = Field(default=None, primary_key=True)             # lomas id
    name: str = Field(max_length=50, unique=True, index=True)   # lomas nosaukums
    description: str = Field(default=None, max_length=100)      # lomas apraksts

# M2M savienojums starp lietotāju un lietotāju lomu
class UserRole(SQLModel, table=True):
    __tablename__ = 'user_roles'                                # lietotāju lomu tabula

    user_id: int = Field(foreign_key="users.id", primary_key=True)        # lietotāja id
    role_id: int = Field(foreign_key="roles.id", primary_key=True)        # lomas id

# Tokenu krātuve
class Token(SQLModel, table=True):
    __tablename__ = 'tokens'          # tokenu krātuve

    # === Tabulas lauki ===
    # ieraksta id
    # lietotāja id
    # atjauninājuma tokens
    # izbeigšanas datums
    # izveidošanas datums

    id: int = Field(default=None, primary_key=True)             
    user_id: int = Field(default=None, foreign_key="users.id")        
    refresh_token: str = Field(max_length=255, index=True)    
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=7))                     
    created_at: datetime = Field(default_factory=utcnow)                       