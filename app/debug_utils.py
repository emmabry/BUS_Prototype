from app import db
from app.models import Student, ExternalAdvisor, Appointment
from datetime import date, time


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
        advisor_objs.append(advisor)

    db.session.flush()

    appointments = [
        Appointment(
            name="Test User",
            email="test@user.com",
            date=date(2025, 4, 16),
            time=time(9, 30),
            reason="Career advice",
            student_id=user_objs[0].id,
            advisor_id=advisor_objs[0].id
        ),
        Appointment(
            name="Emma Test",
            email="emma@email.com",
            date=date(2025, 4, 17),
            time=time(11, 0),
            reason="Work placement discussion",
            student_id=user_objs[2].id,
            advisor_id=advisor_objs[1].id
        )
    ]

    for appt in appointments:
        db.session.add(appt)

    db.session.commit()

