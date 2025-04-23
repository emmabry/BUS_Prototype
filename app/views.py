from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from werkzeug.security import generate_password_hash
import calendar as cal
import datetime as dt
from app import app
from app.models import Student, ExternalAdvisor, Staff, Appointment, Calendar, Event
from app.forms import ChooseForm, LoginForm, SignUpForm, EventForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime
from app.notifications import get_upcoming_events


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
    upcoming_messages = get_upcoming_events(current_user)
    for message in upcoming_messages:
        flash(message, 'info')
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
        db.session.flush()
        user.create_default_calendar()
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


@app.route('/calendar')
def calendar_view():
    year = int(request.args.get('year', dt.datetime.now().year))
    month = int(request.args.get('month', dt.datetime.now().month))

    cal_obj = cal.monthcalendar(year, month)
    month_name = cal.month_name[month]
    calendar = db.session.scalar(sa.select(Calendar).where(Calendar.owner_id == current_user.id))

    events = calendar.get_events_by_month(year, month)

    events_by_date = {}
    for event in events:
        event_date = event.start_time.date()
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append({
            'id': event.id,
            'title': event.title,
            'time': event.start_time.strftime('%H:%M')
        })

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    return render_template(
        'calendar.html',
        year=year,
        month=month,
        month_name=month_name,
        calendar=cal_obj,
        events=events_by_date,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year,
        choose_form=ChooseForm(),
        today=dt.datetime.now().date(),
        datetime=dt.datetime
    )

@app.route('/calendar/view/<int:event_id>', methods=['GET', 'POST'])
@login_required
def view_event(event_id):
    event = db.session.query(Event).get(event_id)
    return render_template('event.html', event=event, title="View Event")

@app.route('/calendar/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.session.query(Event).get(event_id)
    if event:
        form = EventForm(
            title=event.title,
            description=event.description,
            start_date=event.start_time.date(),
            start_time=event.start_time.strftime('%H:%M'),
            end_date=event.end_time.date(),
            end_time=event.end_time.strftime('%H:%M'),
            location=event.location
        )
        if form.validate_on_submit():
            event.title = form.title.data
            event.description = form.description.data
            event.start_time = dt.datetime.combine(form.start_date.data, dt.time.fromisoformat(form.start_time.data))
            event.end_time = dt.datetime.combine(form.end_date.data, dt.time.fromisoformat(form.end_time.data))
            event.location = form.location.data
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('calendar_view'))
        return render_template('generic_form.html', title='Edit Event', form=form)

@app.route('/calendar/delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = db.session.query(Event).get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    else:
        flash('Event not found!', 'danger')
    return redirect(url_for('calendar_view'))

@app.route('/calendar/add', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        start_time = form.start_time.data
        hours, minutes = map(int, start_time.split(':'))
        start_time = dt.datetime.combine(form.start_date.data, dt.time(hours, minutes))
        end_time = form.end_time.data
        hours, minutes = map(int, end_time.split(':'))
        end_time = dt.datetime.combine(form.end_date.data, dt.time(hours, minutes))
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=start_time,
            end_time=end_time,
            location=form.location.data,
            calendar_id=current_user.calendar.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('calendar_view'))
    return render_template('generic_form.html', title='Add Event', form=form)

@app.route('/appointments', methods = ['POST', 'GET'])
@login_required
def appointments():
    user_appointments = Appointment.query.filter_by(student_id=current_user.id).order_by(Appointment.start_time).all()
    return render_template('appointments.html', appointments=user_appointments)


@app.route('/appointment_details/<int:id>')
def appointment_details(id):
    appointment = db.session.get(Appointment, id)
    return render_template('appointment.html', appointment=appointment)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    advisors = ExternalAdvisor.query.all()
    form.advisor_id.choices = [(a.id, f"{a.first_name} {a.last_name} ({a.organisation})") for a in advisors]

    if form.validate_on_submit():
        start_time = dt.datetime.combine(form.date.data, form.time.data)
        end_time = start_time + dt.timedelta(minutes=30)

        advisor = ExternalAdvisor.query.get(form.advisor_id.data)
        appt = Appointment(
            title = f"Appointment with {advisor.first_name} {advisor.last_name}",
            start_time = start_time,
            end_time = end_time,
            description = form.description.data,
            location = form.location.data,
            source = 'appointment',
            student_id = current_user.id,
            advisor_id = form.advisor_id.data,
            calendar_id = current_user.calendar.id
        )
        try:
            db.session.add(appt)
            db.session.commit()
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('appointments'))
        except Exception as e:
            flash(f'Error {e}', 'danger')
            return redirect(url_for('book'))

    return render_template('generic_form.html', title='Book Appointment', form=form)


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
