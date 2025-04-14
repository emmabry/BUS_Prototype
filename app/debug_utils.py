from app import db
from app.models import User
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users = [
        {'first_name': 'Test', 'last_name': 'User',
         'university': 'University of Birmingham',
         'email': 'test@user.com', 'pw': 'test.pw'},
        {'first_name': 'John', 'last_name': 'Smith',
         'university': 'University of Birmingham',
         'email': 'john@email.com', 'pw': 'john.pw'},
        {'first_name': 'Emma', 'last_name': 'Test',
         'university': 'University of Birmingham',
         'email': 'emma@email.com', 'pw': 'emma.pw'}
    ]

    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = User(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)
    db.session.commit()
