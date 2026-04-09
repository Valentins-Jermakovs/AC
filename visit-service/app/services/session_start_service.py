from datetime import datetime
from app.models.activity_models import Session
from app.utils.today import get_today

# ================================================
# Start a new session for a user if there is no active session
# ================================================
async def start_session(user_id: str):
    now = datetime.now()                    # get current time
    activity = await get_today(user_id)    # get today's activity for the user

    # Add a new session only if there is no active session
    if not activity.sessions or activity.sessions[-1].end is not None:
        activity.sessions.append(Session(start=now))  # create new session
        await activity.save()                          # save updated activity