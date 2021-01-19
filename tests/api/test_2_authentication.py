from app.models.User import User
import pytest
from app.utils.DBUtils import get_user_by_name

def register(client, username, password, confirm_password):
    return client.post(
    '/register', data={
    'username' : username,
    'password' : password,
    'confirm_password' : confirm_password,
    'agreement' : True
    },
    follow_redirects=True
    )

def login(client, username, password):
    return client.post(
    '/login', data={
    'username' : username,
    'password' : password
    },
    follow_redirects=True
    )

def logout(client):
    client.get('/logout', follow_redirects=True)

# Assert HTTP code, assert database entry, assert page redirect
def test_valid_register(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD)
    assert response.status_code == 200
    assert get_user_by_name(USERNAME)
    assert b'Dashboard' in response.data
    logout(client)

def test_invalid_register(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'NOTpassword'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD)
    assert response.status_code == 200
    assert b'Create a New Account' in response.data

# Assert HTTP code, assert URL redirect
def test_valid_login(client):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'dashboard' in response.data
    logout(client)

def test_invalid_login(client):
    USERNAME = 'INVALIDUSER'
    PASSWORD = 'wrongpassword'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'The Email Phishing Detection Service' in response.data
