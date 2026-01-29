from fastapi import FastAPI
from contextlib import asynccontextmanager
from .services.init_base import init_db, init_roles
from .routers import auth, users, roles, activity, modifications, google_outh
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

# === programmas sākuma darbības cikls ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()       # inicializē DB ar vajadzīgām tabulām no modeļiem
    await init_roles()    # inicializē lomas
    yield
# === === === === === === === === === ===

# === izveido FastAPI programmas objektu ===
app = FastAPI(lifespan=lifespan)

load_dotenv() # nolasa .env faila saturu
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# === pievieno ceļus (routes) ===
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(modifications.router)
app.include_router(activity.router)
app.include_router(google_outh.router, prefix="/auth")
# === === === === === === === ===


# === Testa funkcionāls (vēlāk izdzēst) ===
@app.get("/")
async def root():
    return {"message": "Hello World"}
# === === === === === === === === === === =
