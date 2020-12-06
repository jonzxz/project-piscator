from app.models.User import User
import pytest

def register(client, username, password, confirm_password):
    return client.post(
    '/register', data={
    'username' : username,
    'password' : password,
    'confirm_password' : confirm_password
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


## Make sure user does not exist in database!!
# Assert HTTP code, assert database entry, assert page redirect
def test_valid_register(client, db):
    response = register(client, 'testuser123', 'password', 'password')
    assert response.status_code == 200
    assert db.session.query(User).filter(User.username == 'testuser123').first()
    assert b'Dashboard' in response.data
    logout(client)

def test_invalid_register(client, db):
    response = register(client, 'testuser123', 'password', 'password')
    assert response.status_code == 200
    assert b'Create a new Account' in response.data

# Assert HTTP code, assert URL redirect
def test_valid_login(client):
    response = login(client, 'user1', 'pa$$w0rd')
    assert response.status_code == 200
    assert b'dashboard' in response.data
    logout(client)

def test_invalid_login(client):
    response = login(client, 'tesaaatuser123', '54321')
    print(response.data)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'The Email Phishing Detection Service' in response.data
