from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    university: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    appointments: so.Mapped[list['Appointment']] = so.relationship('Appointment', back_populates = 'student', cascade='all, delete-orphan')


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ExternalAdvisor(UserMixin, db.Model):
    __tablename__ = 'external_advisors'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    organisation: so.Mapped[str] = so.mapped_column(sa.String(100))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    appointments: so.Mapped[list['Appointment']] = so.relationship('Appointment', back_populates = 'advisor', cascade='all, delete-orphan')

    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    name : so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(120))
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    time: so.Mapped[datetime.time] = so.mapped_column(sa.Time)
    reason: so.Mapped[str] = so.mapped_column(sa.String(200))

    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    student: so.Mapped['User'] = so.relationship('User', back_populates='appointments')

    advisor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('external_advisors.id'))
    advisor: so.Mapped['ExternalAdvisor'] = so.relationship('ExternalAdvisor', back_populates='appointments')


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
