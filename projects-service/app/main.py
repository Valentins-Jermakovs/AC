from fastapi import FastAPI
from .dependencies.database import init_db
from contextlib import asynccontextmanager
# API routers
from .routers import (
    tasks,
    kanban_boards,
    kanban_stages,
    kanban_tasks
)

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

    # (Optional) place cleanup logic here if needed


# =========================
# FastAPI application
# =========================
# Create FastAPI app with custom lifespan logic
app = FastAPI(lifespan=lifespan)

# =========================
# API routers registration
# =========================
# Each router adds its own endpoints to the app
app.include_router(tasks.router)
app.include_router(kanban_boards.router)
app.include_router(kanban_stages.router)
app.include_router(kanban_tasks.router)
