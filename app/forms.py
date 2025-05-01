from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, DateTimeField, RadioField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField, DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    start_date = DateTimeField('Start date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = StringField('Start Time (HH:MM)', validators=[DataRequired(), Length(min=5, max=5)])
    end_date = DateTimeField('End date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    end_time = StringField('End Time (HH:MM))', validators=[DataRequired(), Length(min=5, max=5)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Create Event')

class AppointmentForm(FlaskForm):
    advisor_id = SelectField('Advisor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    description = TextAreaField('Description')
    location = SelectField('Location', choices=[
        ('Online', 'Online'),
        ('In-Person', 'In-Person'),
        ('Phone', 'Phone')
    ], validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class QuizForm(FlaskForm):
    question1 = RadioField('1. I often feel anxious', choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question2 = RadioField('2. I struggle with planning and staying organised', choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question3 = RadioField('3. I often start coursework close to the deadline, and/or submit work late',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question4 = RadioField('4. I find it difficult to focus on my work',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question5 = RadioField('5. I struggle to get started on tasks',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question6 = RadioField('6. It is difficult for me to remember tasks and events',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question7 = RadioField('7. I\'m struggling with finances',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question8 = RadioField('8. It is difficult for me to relax',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question9 = RadioField('9. I often feel overwhelmed',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    question10 = RadioField('10. My mood can change regularly between highs and lows',
                           choices=[(0, 'Never'), (1, 'Rarely'), (2, 'Sometimes'), (3, 'Often'), (4, 'Very Often')])
    submit = SubmitField('Submit')