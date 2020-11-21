from app import app as flask_app

import pytest
import os
import tempfile


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
def Atest_valid_register(client):
    response = register(client, 'user11', 'password', 'password')
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_invalid_register(client):
    response = register(client, 'user1', 'password', 'paassword')
    assert response.status_code == 200
    # assert b'Create a new account' in response.data
