from datetime import datetime, timezone, timedelta

# === datuma un laika iestatīšanas funkcija ===
def utcnow() -> datetime:               # atgriežamā objekta anotācija (priekš SQLModel)
    return datetime.now(timezone.utc)   # datums un laiks UTC