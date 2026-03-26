# Imports
from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional

'''
Participants models

- ParticipantModel: describe a participant

Models are used to define the structure of the data stored in the database, 
and can be used to validate the data before it is saved.
'''

# ===========================
# Participant Model
# ===========================
class ParticipantModel(Document):
    userId: str
    userEmail: str
    eventId: str

    class Settings:
        name = "participants"
        indexes = [
            "eventId",          # Index for event ID
            "userId",           # Index for user ID
        ]