from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField
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