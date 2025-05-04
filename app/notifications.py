from datetime import datetime, timedelta
from app.models import Event
from sqlalchemy import event


class Subscriber:
    def notify(self, event):
        raise NotImplementedError("Subscribers must implement the notify method.")


def get_upcoming_events(user):
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    calendar = user.calendar
    if not calendar:
        return []

    events = calendar.get_events_between(now, one_hour_later)
    notifications = [f"Reminder: upcoming event '{event.title}' at {event.start_time.strftime('%H:%M')}"
                     for event in events]
    return notifications
