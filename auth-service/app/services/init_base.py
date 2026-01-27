from sqlmodel import SQLModel
from ..models.models import User, Role, UserRole, Token
from .base_connection import engine

# Izveido tabulas datu bāzē
SQLModel.metadata.create_all(engine)
