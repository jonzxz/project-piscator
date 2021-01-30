from app.models.User import User
import pytest
from app.utils.DBUtils import get_user_by_name

def register(client, username, password, confirm_password, agreement):
    return client.post(
    '/register', data={
    'username' : username,
    'password' : password,
    'confirm_password' : confirm_password,
    'agreement' : agreement
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

# Test invalid register with empty fields
# Assert HTTP code, assert database entry, assert page redirect
def test_invalid_register_no_input(client, db):
    response = register(client, '', '', '', None)
    assert response.status_code == 200
    assert b'This field is required.', b'You must agree to the terms and\
     policies to register!' in response.data

# Test invalid register with unchecked agreement checkbox
def test_invalid_register_uncheck_checkbox(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD, None)
    assert response.status_code == 200
    assert b'You must agree to the terms and policies to register!' in response.data

# Test invalid register with different passwords
def test_invalid_register_different_passwords(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password1'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD, True)
    assert response.status_code == 200
    assert b'Password must match!' in response.data

# Test valid register
def test_valid_register(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD, True)
    assert response.status_code == 200
    assert get_user_by_name(USERNAME)
    assert b'dashboard' in response.data
    logout(client)

# Test invalid register with existing username
def test_invalid_register_exist(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    response = register(client, USERNAME, PASSWORD, CONF_PASSWORD, True)
    assert response.status_code == 200
    assert b'Username already taken!' in response.data

# Test invalid login with unregistered account
def test_invalid_unregistered_login(client):
    USERNAME = 'testuser123456'
    PASSWORD = 'password'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

# Test invalid login with incorrect password
def test_invalid_password_login(client):
    USERNAME = 'testuser123'
    PASSWORD = 'password123'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

# Test invalid login with empty password
def test_invalid_empty_password_login(client):
    USERNAME = 'testuser123'
    response = login(client, USERNAME, '')
    assert response.status_code == 200
    assert b'Login' in response.data

# Test valid login
def test_valid_login(client):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'dashboard' in response.data
    logout(client)

# Test logout
def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'The Email Phishing Detection Service' in response.data
