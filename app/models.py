from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime as dt

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(50))

    calendar = db.relationship('Calendar', back_populates='owner', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def __repr__(self):
        pwh = 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, first_name={self.first_name}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@dataclass
class Student(User):
    __tablename__ = 'students'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    course: so.Mapped[str] = so.mapped_column(sa.String(100))
    preferences: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    appointments: so.Mapped[list['Appointment']] = so.relationship(
        'Appointment',
        back_populates='student',
        cascade='all, delete-orphan',
        foreign_keys='Appointment.student_id'
    )
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

@dataclass
class Staff(User):
    __tablename__ = 'staff'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    staff_id: so.Mapped[str] = so.mapped_column(sa.String(100))
    department: so.Mapped[str] = so.mapped_column(sa.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

@dataclass
class ExternalAdvisor(User):
    __tablename__ = 'external_advisors'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    organisation: so.Mapped[str] = so.mapped_column(sa.String(100))
    appointments: so.Mapped[list['Appointment']] = so.relationship(
        'Appointment',
        back_populates='advisor',
        cascade='all, delete-orphan',
        foreign_keys='Appointment.advisor_id'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'external_advisors',
    }

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(120))
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date)
    time: so.Mapped[dt.time] = so.mapped_column(sa.Time)
    reason: so.Mapped[str] = so.mapped_column(sa.String(200))

    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    student: so.Mapped['Student'] = so.relationship(
        'Student',
        back_populates='appointments',
        foreign_keys=[student_id]
    )

    advisor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    advisor: so.Mapped['ExternalAdvisor'] = so.relationship(
        'ExternalAdvisor',
        back_populates='appointments',
        foreign_keys=[advisor_id]
    )

class Calendar(db.Model):
    __tablename__ = 'calendars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    color = db.Column(db.String(20), default='#3788d8')  # Default color for the calendar
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', back_populates='calendar')

    # Aggregation relationship with Event
    events = db.relationship('Event', back_populates='calendar', lazy='dynamic')

    def __repr__(self):
        return f'<Calendar {self.name}>'

    def add_event(self, title, start_time, end_time, description=None, location=None):
        """Create and add a new event to this calendar"""
        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
            calendar=self
        )
        db.session.add(event)
        return event

    def get_events_by_date(self, date):
        return self.events.filter(
            db.func.date(Event.start_time) == date
        ).order_by(Event.start_time).all()

    def get_events_by_month(self, year, month):
        start_date = dt.datetime(year, month, 1)
        if month == 12:
            end_date = dt.datetime(year + 1, 1, 1)
        else:
            end_date = dt.datetime(year, month + 1, 1)

        return self.events.filter(
            Event.start_time >= start_date,
            Event.start_time < end_date
        ).order_by(Event.start_time).all()

    def get_events_between(self, start_date, end_date):
        return self.events.filter(
            Event.start_time >= start_date,
            Event.start_time < end_date
        ).order_by(Event.start_time).all()

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_all_day = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    # Foreign key to Calendar
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendars.id'), nullable=False)
    calendar = db.relationship('Calendar', back_populates='events')

    def __repr__(self):
        return f'<Event {self.title}>'

    @property
    def duration(self):
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'is_all_day': self.is_all_day,
            'calendar_id': self.calendar_id
        }

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
