from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from werkzeug.security import generate_password_hash
import calendar as cal
import datetime as dt
from app import app
from app.models import Student, ExternalAdvisor, Staff, Appointment, Calendar, Event, WorkingHour, Quiz
from app.forms import ChooseForm, LoginForm, SignUpForm, EventForm, AppointmentForm, QuizForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime
from app.notifications import get_upcoming_events


# UniSupport landing page
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
    # If there is an upcoming event, a notification for this is displayed
    upcoming_messages = get_upcoming_events(current_user)
    for message in upcoming_messages:
        flash(message, 'info')
    # Get users quiz results
    q = db.select(Quiz).where(Quiz.user_id == current_user.id)
    quiz = db.session.scalars(q).first()
    if quiz:
        quiz_responses = [
            quiz.response1,
            quiz.response2,
            quiz.response3,
            quiz.response4,
            quiz.response5,
            quiz.response6,
            quiz.response7,
            quiz.response8,
            quiz.response9,
            quiz.response10
        ]
    # If a user scored above 3 on a question, a tailored recommendation is displayed
        all_responses_under_three = all(response < 3 for response in quiz_responses)
    else:
        all_responses_under_three = False
    return render_template('dashboard.html', title="Dashboard", quiz=quiz, all_responses_under_three=all_responses_under_three)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Create a new student user in database
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
        # Log in user
        login_user(user)
        flash('Your account has been created!', 'success')
        # Prompt new user to take onboarding quiz
        return redirect(url_for('quiz'))
    return render_template('signup.html', title="Sign Up", form=form)

@app.route('/start_quiz')
def start_quiz():
    return render_template('start_quiz.html', title="Start Quiz")

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    q = db.select(Quiz).where(Quiz.user_id == current_user.id)
    quiz = db.session.scalars(q).first()
    if form.validate_on_submit():
        if quiz:
            # If user has already submitted quiz, update their answers
            quiz.response1 = form.question1.data
            quiz.response2 = form.question2.data
            quiz.response3 = form.question3.data
            quiz.response4 = form.question4.data
            quiz.response5 = form.question5.data
            quiz.response6 = form.question6.data
            quiz.response7 = form.question7.data
            quiz.response8 = form.question8.data
            quiz.response9 = form.question9.data
            quiz.response10 = form.question10.data
        else:
            # If first time, create a new entry in the quiz table with the users answers
            quiz_answers = Quiz(
                response1=form.question1.data,
                response2=form.question2.data,
                response3=form.question3.data,
                response4=form.question4.data,
                response5=form.question5.data,
                response6=form.question6.data,
                response7=form.question7.data,
                response8=form.question8.data,
                response9=form.question9.data,
                response10=form.question10.data,
                student=current_user
            )
            db.session.add(quiz_answers)
        db.session.commit()
        flash(f'Quiz submitted!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('quiz.html', title="Onboarding Quiz", form=form, quiz=quiz)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Check user email is in database
        user = db.session.scalar(
            sa.select(Student).where(Student.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    return render_template('generic_form.html', title='Sign In', form=form)


@app.route('/calendar')
@login_required
def calendar_view():
    # Get current year and month
    year = int(request.args.get('year', dt.datetime.now().year))
    month = int(request.args.get('month', dt.datetime.now().month))

    # Initiate calendar object and get calendar data from DB
    calendar = cal.monthcalendar(year, month)
    month_name = cal.month_name[month]
    calendar_data = db.session.scalar(sa.select(Calendar).where(Calendar.owner_id == current_user.id))

    # Get event data for current month
    events = calendar_data.get_events_by_month(year, month)

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

    # Fix calendar so that it loops back to the previous December if clicking backwards from January
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    # Fix calendar so it correctly goes to the following year after December
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
        calendar=calendar,
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
    # Get event by id from database
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
            # Update event data with new form data
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
        # Remove event from database
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
        # Add new event to database
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
    # Get users current appointments from database
    user_appointments = Appointment.query.filter_by(student_id=current_user.id).order_by(Appointment.start_time).all()
    return render_template('appointments.html', appointments=user_appointments)


@app.route('/appointment_details/<int:id>')
def appointment_details(id):
    # Get appointment from database using id
    appointment = db.session.get(Appointment, id)
    return render_template('appointment.html', appointment=appointment)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    advisors = ExternalAdvisor.query.all()
    # Display advisors to choose for appointment
    form.advisor_id.choices = [(a.id, f"{a.first_name} {a.last_name} ({a.organisation})") for a in advisors]

    if form.validate_on_submit():
        start_datetime = dt.datetime.combine(form.date.data, form.time.data)
        end_datetime = start_datetime + dt.timedelta(minutes=30)

        # Check if there is a preexisting event which overlaps with appointment
        student_conflict = Event.query.filter(
            Event.calendar_id == current_user.calendar.id,
            Event.start_time < end_datetime,
            Event.end_time > start_datetime
        ).first()

        if student_conflict:
            flash('There is already and event on your calender during that time. Please choose another slot.', 'danger')
            return render_template('generic_form.html', form = form)

        advisor = ExternalAdvisor.query.get(form.advisor_id.data)
        advisor_calendar = advisor.calendar
        advisor_conflict = Event.query.filter(
            Event.calendar_id == advisor_calendar.id,
            Event.start_time < end_datetime,
            Event.end_time > start_datetime
        ).first()

        if advisor_conflict:
            flash("The advisor already has an event during that time. Please choose another slot", 'danger')
            return render_template('generic_form.html', form = form)

        # Check if advisor has availability
        day_of_week = start_datetime.weekday()
        working_hour = WorkingHour.query.filter_by(advisor_id=advisor.id, day_of_week = day_of_week).first()

        if not working_hour:
            flash('The advisor is not available on that day', 'danger')
            return render_template('generic_form.html', form=form)

        if not (working_hour.start_time <= start_datetime.time() < working_hour.end_time and
        working_hour.start_time < end_datetime.time() <= working_hour.end_time):
            flash("The selected time is outside the advisor's working hours", 'danger')
            return render_template('generic_form.html', form = form)

        # Add new appointment to database
        appt = Appointment(
            title = f"Appointment with {advisor.first_name} {advisor.last_name}",
            start_time = start_datetime,
            end_time = end_datetime,
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

@app.route('/help_centre')
def help_centre():
    return render_template('help_centre.html')

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
