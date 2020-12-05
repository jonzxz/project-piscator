from app import app as flask_app
from app import db
from app.models.User import User

import pytest
import os

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()

def register(client, username, password, confirm_password):
    return client.post(
    '/register', data={
    'username' : username,
    'password' : password,
    'confirm_password' : confirm_password
    },
    follow_redirects=True
    )

## Make sure user does not exist in database!!
# Assert HTTP code, assert database entry, assert page redirect
def test_valid_register(client):
    response = register(client, 'testuser123', 'password', 'password')
    assert response.status_code == 200
    assert db.session.query(User).filter(User.username == 'testuser123').first()
    assert b'Dashboard' in response.data

def test_invalid_register(client):
    response = register(client, 'testuser123', 'password', 'password')
    assert response.status_code == 200
    assert b'Create a new Account' in response.data
