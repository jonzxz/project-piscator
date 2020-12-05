from app import app as flask_app
from test_3_login import login

import pytest

from app import db
from app.models.EmailAddress import EmailAddress

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    # WTF_CSRF_ENABLED = False to allow form submission in tests
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()

def add_mail(client, email, password):
    return client.post(
    '/dashboard/emails', data={
    'email_address' : email,
    'password' : password
    },
    follow_redirects=True
    )

# Make sure user is valid and email does not exist in database
# Assert HTTP code, assert database entry, assert new mail displayed in page
def test_valid_add_mail(client):
    login(client, 'testuser123', 'password')
    response = add_mail(client, 'testmail456@mymail.com', 'password')

    assert response.status_code == 200
    assert db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    assert b'testmail456@mymail.com' in response.data
