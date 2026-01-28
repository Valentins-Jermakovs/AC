from sqlmodel import Field, SQLModel
from datetime import datetime, timezone, timedelta

# === datuma un laika iestatīšanas funkcija ===
def utcnow() -> datetime:               # atgriežamā objekta anotācija (priekš SQLModel)
    return datetime.now(timezone.utc)   # datums un laiks UTC
# === === === === === === === === === === === ===

# === MODEĻI ===

# === Lietotāja modelis ===
class User(SQLModel, table=True):
    __tablename__ = 'users'                                         # tabulas nosaukums

    id: int = Field(primary_key=True)                               # lietotāja ID
    username: str = Field(max_length=50, index=True, unique=True)   # lietotāja vārds
    password_hash: str = Field(max_length=255)                      # lietotāja parole
    email: str = Field(max_length=100, index=True, unique=True)     # lietotāja e-pasts
    created_at: datetime = Field(default_factory=utcnow)            # lietotāja izveide datums
    active: bool = Field(default=True)                              # lietotāja statuss
# === === === === === ===

# === Lomu modelis ===
class Role(SQLModel, table=True):
    __tablename__ = 'roles'                                     # tabulas nosaukums

    id: int = Field(primary_key=True)                           # lomas ID
    name: str = Field(max_length=50, unique=True, index=True)   # lomas nosaukums
    description: str = Field(max_length=100)                    # lomas apraksts
# === === === === ===

# === M2M savienojums starp lietotāju un lietotāju lomu ===
class UserRole(SQLModel, table=True):
    __tablename__ = 'user_roles'                                          # lietotāju lomu tabula

    user_id: int = Field(foreign_key="users.id", primary_key=True)        # lietotāja id
    role_id: int = Field(foreign_key="roles.id", primary_key=True)        # lomas id
# === === === === === === === === === === === === === ===

# === Tokenu krātuve ====
class Token(SQLModel, table=True):
    __tablename__ = 'tokens'          # tabulas nosaukums

    # === Tabulas lauki ===
    # ieraksta ID
    # lietotāja ID
    # atjauninājuma tokens
    # tokena izbeigšanas datums
    # tokena izveidošanas datums

    id: int = Field(default=None, primary_key=True)             
    user_id: int = Field(default=None, foreign_key="users.id")        
    refresh_token: str = Field(max_length=255, index=True)    
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=7))                     
    created_at: datetime = Field(default_factory=utcnow)
# === === === === === === === === === === === === === ===                      