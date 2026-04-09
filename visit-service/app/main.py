from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.dependencies.database import init_db

from app.routes import router

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

# =========================
# API endpoints
# =========================
# Each router adds its own endpoints to the app
app.include_router(router.router)