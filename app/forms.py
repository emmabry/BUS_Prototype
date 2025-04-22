from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, DateTimeField
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
