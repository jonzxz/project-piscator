from app import app as flask_app

import pytest

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    # WTF_CSRF_ENABLED = False to allow form submission in tests
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()

def login(client, username, password):
    return client.post(
    '/login', data={
    'username' : username,
    'password' : password
    },
    follow_redirects=True
    )

def add_mail(client, email, password):
    return client.post(
    '/dashboard/emails', data={
    'email_address' : email,
    'password' : password
    },
    follow_redirects=True
    )

# Make sure user is valid and email does not exist in database
def test_valid_add_mail(client):
    login(client, 'user1', 'password')
    response = add_mail(client, 'huat@nomail123.com', 'password')
    assert response.status_code == 200
    assert b'huat@nomail123.com' in response.data
