from test_2_authentication import login
from app.models.EmailAddress import EmailAddress
from app.utils.FileUtils import get_server_mail_cred

import pytest

def add_mail(client, email, password):
    return client.post(
    '/dashboard/emails', data={
    'email_address' : email,
    'password' : password
    },
    follow_redirects=True
    )

def enable_disable_mail(client, mail_id):
    return client.get('/dashboard/emails/activation/{}'.format(mail_id), follow_redirects=True)

def detection_check(client, mail_id):
    return client.get('/dashboard/emails/phish/{}'.format(mail_id), follow_redirects=True)

def detection_history(client, mail_id):
    return client.get('/dashboard/emails/history/{}'.format(mail_id), follow_redirects=True)

# Make sure user is valid and email does not exist in database
# Assert HTTP code, assert database entry, assert new mail displayed in page
def test_valid_add_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]

    login(client, USERNAME, PASSWORD)
    response = add_mail(client, EMAIL_ADDR, EMAIL_PASSWORD)
    assert response.status_code == 200
    assert db.session.query(EmailAddress).filter(EmailAddress.email_address == EMAIL_ADDR).first()
    assert b'piscator.fisherman@gmail.com' in response.data

def test_check_email(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]


    login(client, USERNAME, PASSWORD)
    mail_address = EmailAddress.query.filter(EmailAddress.email_address == 'piscator.fisherman@gmail.com').first()
    mail_id = mail_address.get_email_id()
    response = detection_check(client, mail_id)
    assert response.status_code == 200
    assert b'Detection Results' in response.data

def test_detection_history(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]


    login(client, USERNAME, PASSWORD)
    mail_address = EmailAddress.query.filter(EmailAddress.email_address == 'piscator.fisherman@gmail.com').first()
    mail_id = mail_address.get_email_id()
    response = detection_history(client, mail_id)
    assert response.status_code == 200
    assert b'Detection History' in response.data

def test_valid_disable_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    login(client, USERNAME, PASSWORD)

    mail_address = EmailAddress.query.filter(EmailAddress.email_address == 'piscator.fisherman@gmail.com').first()
    mail_id = mail_address.get_email_id()
    response = enable_disable_mail(client, mail_id)
    updated_status = EmailAddress.query.filter(EmailAddress.email_address == 'piscator.fisherman@gmail.com').first().get_active_status()
    assert response.status_code == 200
    assert updated_status == False
