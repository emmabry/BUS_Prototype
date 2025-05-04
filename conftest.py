import pytest
from app import app as flask_app, db

@pytest.fixture(scope='session')
def app():
    with flask_app.app_context():
        yield flask_app