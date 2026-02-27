# =========================
# Main application entry
# =========================

# Import FastAPI main class
from fastapi import FastAPI
# Used to manage application startup and shutdown lifecycle
from contextlib import asynccontextmanager
# Middleware for server-side sessions (cookies, session storage)
from starlette.middleware.sessions import SessionMiddleware

# Standard libraries
import os
# Loads environment variables from .env file
from dotenv import load_dotenv
# Function that initializes database connection / tables
from .utils.init_data_base import init_db

# Import all API routers (each router = separate feature)
from .routers import (
    auth_route,           # login / authentication endpoints
    refresh_route,        # refresh token logic
    read_users_route,     # get user data
    modify_user_route,    # update user data
    activity_route,       # user activity management (deactivate / activate)
    roles_route           # user roles and permissions
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
# Environment & middleware
# =========================
# Load variables from .env file into environment
load_dotenv()

# Add session middleware
# Used for session-based authentication or temporary user data
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


# =========================
# API routers registration
# =========================
# Each router adds its own endpoints to the app

app.include_router(auth_route.router)             # /auth/*
app.include_router(refresh_route.router)          # /refresh/*
app.include_router(read_users_route.router)       # /users/*
app.include_router(modify_user_route.router)      # /modify/*
app.include_router(activity_route.router)         # /activity/*
app.include_router(roles_route.router)            # /roles/*