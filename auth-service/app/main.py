from fastapi import FastAPI
from contextlib import asynccontextmanager
from .services.init_base import init_db, init_roles
from .routers import auth, users

# === programmas sākuma darbības cikls ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()       # inicializē DB ar vajadzīgām tabulām no modeļiem
    await init_roles()    # inicializē lomas
    yield
# === === === === === === === === === ===

# === izveido FastAPI programmas objektu ===
app = FastAPI(lifespan=lifespan)

# === pievieno ceļus (routes) ===
app.include_router(auth.router)
app.include_router(users.router)
# === === === === === === === ===


# === Testa funkcionāls (vēlāk izdzēst) ===
@app.get("/")
async def root():
    return {"message": "Hello World"}
# === === === === === === === === === === =
