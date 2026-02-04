from datetime import datetime, timezone

# date and time util
# get current date
def get_current_date():
    return datetime.now(timezone.utc)
