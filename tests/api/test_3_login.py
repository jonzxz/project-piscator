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

# Assert HTTP code, assert URL redirect
def test_valid_login(client):
    response = login(client, 'testuser123', 'password')
    assert response.status_code == 200
    assert b'dashboard' in response.data

def test_invalid_login(client):
    response = login(client, 'testuser123', '54321')
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
