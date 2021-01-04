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

def test_invalid_login(client):
    USERNAME = 'INVALIDADMIN'
    PASSWORD = 'NOTpassword'
    response = login(client, USERNAME, PASSWORD)
    assert response.status_code == 200
    assert not b'Administrator Dashboard' in response.data
