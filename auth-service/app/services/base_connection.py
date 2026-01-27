from sqlmodel import create_engine
import os
from dotenv import load_dotenv


# Šis fails atbilst par savienojuma izveidi ar DB

load_dotenv() # nolad .env faila saturu

DATABASE_URL = os.getenv("DATABASE_URL") # paņemam no .env
engine = create_engine(DATABASE_URL, echo=True)

# Ja FastAPI serveris pats darbojas Docker konteinerī, 
# tad localhost vietā jānorāda MySQL konteineru nosaukums, 
# piemēram auth_mysql.