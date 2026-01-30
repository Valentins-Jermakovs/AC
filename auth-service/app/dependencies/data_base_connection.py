# ===== Importi =====
from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv

# ===== dotenv faila satura apstrāde =====
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# ===== DB savienojuma izveide =====
def get_db():                   
    session = Session(engine)   
    try:                        
        yield session
    finally:                    
        session.close()

# Ja FastAPI serveris darbosies kā Docker konteineris, 
# tad localhost vietā nor norādi DB servera konteineru nosauku,
# piemēram auth_postgres