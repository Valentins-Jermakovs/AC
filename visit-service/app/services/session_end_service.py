from datetime import datetime
from app.utils.today import get_today

# ================================================
# End the current active session for a user
# ================================================
async def end_session(user_id: str):
    now = datetime.now()                    # get current time
    activity = await get_today(user_id)    # get today's activity for the user

    # If there are no sessions or the last session is already closed
    if not activity.sessions or activity.sessions[-1].end is not None:
        return  # no active session to end

    # Get the last session
    session = activity.sessions[-1]

    # Close the session and calculate duration
    session.close(now)

    # Add session duration to the total daily seconds
    activity.total_seconds += session.duration

    # Save the updated activity to the database
    await activity.save()