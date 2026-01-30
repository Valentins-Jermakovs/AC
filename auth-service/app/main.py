# ===== Importi =====
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from .services.init_base import (
    init_db,
    init_roles
)

from .routers import (
    auth,
    users,
    roles,
    modifications,
    activity,
    google_outh
)

# ===== Programmas sākuma darbības cikls ===
# DB inicializācijas procesi
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_roles()    
    yield


app = FastAPI(lifespan=lifespan)

# ===== dotenv faila satura apstrāde =====
load_dotenv()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# ===== Pievieno ceļus (routes) =====
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(modifications.router)
app.include_router(activity.router)
app.include_router(google_outh.router)


# ===== Testa funkcionāls (vēlāk izdzēst) =====
@app.get("/")
async def root():
    return {"message": "Hello World"}
