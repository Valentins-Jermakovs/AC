# =========================
# IMPORTS
# =========================
from pymongo import AsyncMongoClient, monitoring
from beanie import init_beanie
import os
from dotenv import load_dotenv

# Models
from app.models.news_model import NewsModel


# =========================
# LOG COLORS
# =========================
# Simple ANSI color codes for console logging
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# =========================
# LOAD ENV VARIABLES
# =========================
# Load environment variables from .env file
load_dotenv()


# =========================
# MONGO LOGGER
# =========================
# This class will listen to all MongoDB commands
# and print status messages in the console
# =========================
class MongoLogger(monitoring.CommandListener):
    """
    MongoDB command logger.
    Logs every command:
    - started
    - succeeded
    - failed
    """

    # -------------------------
    # Command started
    # -------------------------
    def started(self, event):
        print(f"{bcolors.OKCYAN}[MongoDB STARTED] {event.command_name}{bcolors.ENDC}")

    # -------------------------
    # Command succeeded
    # -------------------------
    def succeeded(self, event):
        print(f"{bcolors.OKGREEN}[MongoDB SUCCEEDED] {event.command_name}{bcolors.ENDC}")

    # -------------------------
    # Command failed
    # -------------------------
    def failed(self, event):
        print(f"{bcolors.FAIL}[MongoDB FAILED] {event.command_name} - {event.failure}{bcolors.ENDC}")


# =========================
# DATABASE INITIALIZATION
# =========================
async def init_db():
    """
    Initialize MongoDB connection and Beanie ODM.
    
    Steps:
    1. Register MongoDB logger to track commands
    2. Connect to MongoDB using AsyncMongoClient
    3. Get database instance from client
    4. Initialize Beanie with models
    """
    
    # -------------------------
    # Register Mongo logger
    # -------------------------
    monitoring.register(MongoLogger())

    # -------------------------
    # Connect to MongoDB
    # -------------------------
    mongo_url = os.getenv("MONGO_URL")  # Mongo connection string from .env
    db_name = os.getenv("DB_NAME")      # Database name from .env
    client = AsyncMongoClient(mongo_url)
    db = client[db_name]

    # -------------------------
    # Initialize Beanie ODM
    # -------------------------
    # Pass database instance and document models
    await init_beanie(
        database=db,
        document_models=[
            NewsModel  # add more models here if needed
        ]
    )

    print(f"{bcolors.OKGREEN}MongoDB and Beanie initialized successfully!{bcolors.ENDC}")