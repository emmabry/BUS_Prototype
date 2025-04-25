from app import db
from app.models import Student, ExternalAdvisor, Appointment, WorkingHour
import datetime as dt


def reset_db():
    db.drop_all()
    db.create_all()

    users = [
        {'first_name': 'Test', 'last_name': 'User',
         'email': 'test@user.com', 'pw': 'test.pw',
         'role': 'student', 'course': 'Computer Science'},
        {'first_name': 'John', 'last_name': 'Smith',
         'email': 'john@email.com', 'pw': 'john.pw',
         'role': 'student', 'course': 'Computer Science'},
        {'first_name': 'Emma', 'last_name': 'Test',
         'email': 'emma@email.com', 'pw': 'emma.pw',
         'role': 'student', 'course': 'Computer Science'}
    ]

    user_objs = []
    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = Student(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)
        db.session.flush()
        user.create_default_calendar()
        user_objs.append(user)


    advisors = [
        {'first_name': 'Sam', 'last_name': 'Smith',
         'email': 'sam@external.org', 'organisation': 'Career Services', 'pw': 'sam.pw'},
        {'first_name': 'Mia', 'last_name': 'Lee',
         'email': 'mia@external.org', 'organisation': 'Wellbeing Support', 'pw': 'mia.pw'}
    ]

    advisor_objs = []
    for a in advisors:
        pw = a.pop('pw')
        advisor = ExternalAdvisor(**a)
        advisor.set_password(pw)
        db.session.add(advisor)
        db.session.flush()
        advisor.create_default_calendar()
        advisor_objs.append(advisor)

    db.session.flush()

    for advisor in advisor_objs:
        for day in range(0, 5):
            wh = WorkingHour(
                advisor_id=advisor.id,
                day_of_week = day,
                start_time = dt.time(9, 0),
                end_time = dt.time(17, 0)
            )
            db.session.add(wh)

    appointments = [
        Appointment(
            email="test@user.com",
            start_time=dt.datetime(2025, 4, 18, 9, 0),
            end_time=dt.datetime(2025, 4, 18, 10, 0),
            title=f"Appointment with {advisor_objs[1].first_name} {advisor_objs[1].last_name}",
            description="Career advice",
            location="Online",
            source="appointment",
            student_id=user_objs[0].id,
            advisor_id=advisor_objs[1].id,
            calendar_id=user_objs[0].calendar.id
        ),
        Appointment(
            email="emma@email.com",
            start_time=dt.datetime(2025, 4, 20, 13, 0),
            end_time=dt.datetime(2025, 4, 20, 13, 30),
            title=f"Appointment with {advisor_objs[1].first_name} {advisor_objs[1].last_name}",
            description="Work placement discussion",
            source="appointment",
            student_id=user_objs[2].id,
            advisor_id=advisor_objs[1].id,
            calendar_id=user_objs[2].calendar.id
        )
    ]

    for appt in appointments:
        db.session.add(appt)

        # AMY REMOVE // placeholder for upcoming event V

    for appt in appointments:
        db.session.add(appt)

    now = dt.datetime.now()
    john_soon_appt = Appointment(
        email="john@email.com",
        start_time=now + dt.timedelta(minutes=59),
        end_time=now + dt.timedelta(minutes=89),
        title="Test Reminder Appointment",
        description="This is a test appointment to trigger notification.",
        location="Online",
        source="appointment",
        student_id=user_objs[1].id,  # John
        advisor_id=advisor_objs[0].id,
        calendar_id=user_objs[1].calendar.id
    )
    db.session.add(john_soon_appt)

    # AMY REMOVE ^

    db.session.commit()

