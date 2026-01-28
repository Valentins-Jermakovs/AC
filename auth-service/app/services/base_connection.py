from sqlmodel import create_engine
import os
from dotenv import load_dotenv


# === Šis fails atbilst par savienojuma izveidi ar DB ===

load_dotenv() # nolasa .env faila saturu

DATABASE_URL = os.getenv("DATABASE_URL")        # paņem DB URL no .env
engine = create_engine(DATABASE_URL, echo=True) # izveido savienojumu

# create_engine() - izveido savienojumu ar DB
# echo=True - izvada SQL komandas konsolē

# Ja FastAPI serveris pats darbojas Docker konteinerī, 
# tad localhost vietā jānorāda MySQL konteineru nosaukums, 
# piemēram auth_mysql.

# === === === === === === === === === === === === === === ===