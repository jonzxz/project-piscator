from app.models.User import User
import pytest
from test_2_authentication import login

# Assert HTTP code, assert URL redirect
def test_valid_login(client):
    USERNAME = 'admin'
    PASSWORD = 'password'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert b'Administrator Dashboard' in response.data

def test_view_users(client):
    return client.post(
    '/admin/user',
    follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Users' in response.data

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'The Email Phishing Detection Service' in response.data
