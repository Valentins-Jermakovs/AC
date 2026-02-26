# =========================
# Date and time utilities
# =========================
from datetime import datetime, timezone


# =========================
# Current UTC date & time
# =========================
def get_current_date():
    """
    Returns current date and time in UTC timezone.

    Why UTC:
    - Avoids timezone-related bugs
    - Safe for databases and tokens
    - Can be converted to local time later if needed
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
