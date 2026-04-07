from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.dependencies.database import init_db

# =========================
# Application lifespan
# =========================
# This function runs on app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database when application starts
    await init_db()
    # Application works while this yield exists
    yield

# =========================
# FastAPI application
# =========================
# Create FastAPI app with custom lifespan logic
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
