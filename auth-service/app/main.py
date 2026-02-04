# Imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from .utils.init_data_base import init_db

from .routers import (
    auth,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield


app = FastAPI(lifespan=lifespan)

load_dotenv()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(auth.router)