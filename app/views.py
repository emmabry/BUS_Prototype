from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from werkzeug.security import generate_password_hash

from app import app
from app.models import Student, ExternalAdvisor, Staff, Appointment
from app.forms import ChooseForm, LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime


@app.route("/")
def home():
    return render_template('home.html', title="UniSupport")


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title="Dashboard")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            university=form.university.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data, method='pbkdf2')
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('quiz'))
    return render_template('signup.html', title="Sign Up", form=form)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('quiz.html', title="Onboarding Quiz")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Student).where(Student.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route('/appointments', methods = ['POST', 'GET'])
@login_required
def appointments():
    user_appointments = Appointment.query.filter_by(student_id = current_user.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('appointments.html', appointments = user_appointments)


@app.route('/appointment_details/<int:id>')
def appointment_details(id):
    appointment = db.session.get(Appointment, id)
    return render_template('appointment.html', appointment = appointment)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
