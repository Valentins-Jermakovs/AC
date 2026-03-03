# Imports
from fastapi import FastAPI
from .dependencies.database import init_db
from contextlib import asynccontextmanager
# API routers
from .routers.tasks import tasks_route
from .routers.kanban import (
    kanban_boards_route, 
    kanban_members_route,
    kanban_stages_route,
    kanban_tasks_route
)
from .routers.workspaces import (
    workspace_projects_route,
    workspace_members_route
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
app.include_router(tasks_route.router)
app.include_router(kanban_boards_route.router)
app.include_router(kanban_members_route.router)
app.include_router(kanban_stages_route.router)
app.include_router(kanban_tasks_route.router)
app.include_router(workspace_projects_route.router)
app.include_router(workspace_members_route.router)
