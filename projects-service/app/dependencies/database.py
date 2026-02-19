# Imports
from pymongo import AsyncMongoClient, monitoring
from beanie import init_beanie
import os
from dotenv import load_dotenv
from ..models import PrivateTaskModel

# Colors for logging
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

# Load environment variables
load_dotenv()

# =========================
# MongoDB logger:
# - started
# - succeeded
# - failed
#
# This function is global. It will be called for every command
# executed on the database.
# =========================
class MongoLogger(monitoring.CommandListener):
    # command started
    def started(self, event):
        print(f"{bcolors.OKCYAN}[MongoDB STARTED] {event.command_name}{bcolors.ENDC}")

    # command succeeded
    def succeeded(self, event):
        print(f"{bcolors.OKGREEN}[MongoDB SUCCEEDED] {event.command_name}{bcolors.ENDC}")

    # command failed
    def failed(self, event):
        print(f"{bcolors.FAIL}[MongoDB FAILED] {event.command_name} - {event.failure}{bcolors.ENDC}")

# =========================
# Initialize database
# =========================
async def init_db():
    # Register logger
    monitoring.register(MongoLogger())

    # Connect to database
    client = AsyncMongoClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("DB_NAME")]

    # Initialize database
    await init_beanie(
        database=db,
        document_models=[PrivateTaskModel]
    )
