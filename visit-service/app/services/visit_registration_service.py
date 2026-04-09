from datetime import datetime, date
from app.models.activity_models import UserDailyActivity, Session
from app.utils.today import get_today

# ================================================
# Register a user visit: update sessions and daily activity
# ================================================
async def register_visit(user_id: str):
    now = datetime.now()                     # get current time
    activity = await get_today(user_id)     # get today's activity for the user

    # Add a new session if there is no active session
    if not activity.sessions or activity.sessions[-1].end is not None:
        activity.sessions.append(Session(start=now))

    # Update last visit time and visit count
    activity.last_visit = now
    activity.visit_count += 1

    # Save updated activity to the database
    await activity.save()