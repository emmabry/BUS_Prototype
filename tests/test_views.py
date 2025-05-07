import pytest
from flask import url_for
from app import app, db
from app.debug_utils import reset_db
from app.models import Student, Quiz

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

@pytest.fixture(scope='function')
def setup_db():
    with app.app_context():
        reset_db()
        yield
        db.session.remove()

def login_test_user(client, email='test@user.com', password='test.pw'):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_dashboard_positive(setup_db):
    with app.test_client() as client:
        login_test_user(client)
        response = client.get('/dashboard')
        assert b"quiz" in response.data or b"response" in response.data or b"title=\"Dashboard\"" in response.data


def test_dashboard_negative(setup_db):
    with app.test_client() as client:
        response = client.get('/dashboard', follow_redirects=True)
        assert b"Sign In" in response.data

def test_signup_positive(setup_db):
    with app.test_client() as client:
        response = client.post('/signup', data={
            'first_name': 'amy',
            'last_name': 'baker',
            # 'university': 'test uni',
            'course': 'test',
            'email': 'amy@birmingham.com',
            'password': 'test123',
'confirm_password': 'test123',
            'submit': True

        }, follow_redirects=True)
        assert b"Your account has been created!" in response.data

def test_signup_negative(setup_db):
    with app.test_client() as client:
        response = client.post('/signup', data={
            'first_name': 'amy',
            'last_name': 'baker',
            # 'university': '',
            'course': '',
            'email': 'amy@birmingham.com',
            'password': 'test123',
            'confirm_password': 'test123wrong',

        }, follow_redirects=True)
        assert (
            b'This field is required.' in response.data or
            b'Field must be equal to password.' in response.data
        )

def test_calendar_positive(setup_db):
    with app.test_client() as client:
        login_test_user(client)
        response=client.get('/calendar')
        assert b"<table" in response.data

def test_calendar_negative(setup_db):
    with app.test_client() as client:
        response = client.get('/calendar', follow_redirects=True)
        assert response.request.path == '/login'

def test_quiz_positive(setup_db):
    with app.test_client() as client:
        login_test_user(client)
        response = client.post('/quiz', data={
            'question1': '3',
            'question2': '2',
            'question3': '1',
            'question4': '4',
            'question5': '0',
            'question6': '1',
            'question7': '2',
            'question8': '3',
            'question9': '2',
            'question10': '1',
        }, follow_redirects=True)
        assert b"Quiz submitted!" in response.data

def test_quiz_negative(setup_db):
    with app.test_client() as client:
        login_test_user(client)
        response = client.post('/quiz', data={})
        assert b"Redirecting" in response.data or response.status_code == 200

def test_appointments_positive(setup_db):
    with app.test_client() as client:
        login_test_user(client)
        response = client.get('/appointments')
        assert b"Appointment" in response.data or b"appointment" in response.data


def test_appointments_negative(setup_db):
    with app.test_client() as client:
        response = client.get('/appointments', follow_redirects=True)
        assert b"Sign In" in response.data
