from sqlmodel import Field, Session, SQLModel, create_engine, select

# lietotāja modelis
class User(SQLModel):
    __tablename__ = 'users'                                     # lietotāja tabula

    id: int = Field(default=None, primary_key=True)             # lietotāja id
    username: str = Field(default=None, max_length=50)          # lietotāja vards
    password_hash: str = Field(default=None, max_length=20)     # lietotāja parole
    email: str = Field(default=None, max_length=20)             # lietotāja e-pasts
    created_at: str = Field(default=None)                       # lietotāja reģistrēšanas datums
    active = Field(default=False)                               # lietotāja statuss

# lomas modelis
class Role(SQLModel):
    __tablename__ = 'roles'                                     # lietotāju lomu tabula

    id: int = Field(default=None, primary_key=True)             # lomas id
    name: str = Field(default=None, max_length=50)              # lomas nosaukums
    description: str = Field(default=None, max_length=100)      # lomas apraksts

# M2M savienojums starp lietotāju un lietotāju lomu
class UserRole(SQLModel):
    __tablename__ = 'user_roles'                                # lietotāju lomu tabula

    user_id: int = Field(default=None, primary_key=True)        # lietotāja id
    role_id: int = Field(default=None, primary_key=True)        # lomas id

# Tokenu krātuve
class Token(SQLModel):
    __tablename__ = 'tokens'                                    # lietotāju lomu tabula

    id: int = Field(default=None, primary_key=True)             # ieraksta id
    user_id: int = Field(default=None, primary_key=True)        # lietotāja id
    refresh_token: str = Field(default=None, max_length=100)    # atjauninājuma tokens
    expires_at: str = Field(default=None)                       # izbeigšanas datums
    created_at: str = Field(default=None)                       # izveidošanas datums