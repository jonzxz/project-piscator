import pytest
from app import app as flask_app
from app import db as ps_db

@pytest.fixture(scope='session')
def app():
    yield flask_app

@pytest.fixture(scope='session')
def client(app):
    # WTF_CSRF_ENABLED = False to allow form submission in tests
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture(scope='session')
def db():
    yield ps_db
