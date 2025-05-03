import pytest
from datetime import datetime, timedelta
from app import db
from app.models import Student, ExternalAdvisor, Appointment
from app.notifications import get_upcoming_events
from app.debug_utils import reset_db


@pytest.fixture(scope='function')
def setup_db(app):
    reset_db()
    yield
    db.session.remove()


def test_get_upcoming_events_positive(app, setup_db):
    student = Student.query.filter_by(email="john@email.com").first()
    advisor = ExternalAdvisor.query.first()

    now = datetime.now()
    appointment = Appointment(
        email=student.email,
        start_time=now + timedelta(minutes=45),
        end_time=now + timedelta(minutes=75),
        title="Reminder: Upcoming Test Appointment",
        description="This should trigger a notification.",
        location="Online",
        source="appointment",
        student_id=student.id,
        advisor_id=advisor.id,
        calendar_id=student.calendar.id
    )

    db.session.add(appointment)
    db.session.commit()

    notifications = get_upcoming_events(student)
    assert len(notifications) == 1
    assert "Reminder: Upcoming Test Appointment" in notifications[0]


def test_get_upcoming_events_negative(app, setup_db):
    student = Student.query.filter_by(email="emma@email.com").first()
    notifications = get_upcoming_events(student)
    assert notifications == []
