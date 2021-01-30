import pytest
from app.models.User import User
from app.models.EmailAddress import EmailAddress

@pytest.fixture()
def user():
    user = User(username='testuser123')
    user.set_password('password1')
    return user

@pytest.fixture()
def email_addr():
    email_addr = EmailAddress(email_address='testmail@nomail.com')
    email_addr.set_email_password('verySecureP@$$w0rd')
    return email_addr
