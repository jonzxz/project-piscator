from test_2_authentication import login
from app.models.EmailAddress import EmailAddress
from app.utils.FileUtils import get_server_mail_cred
from app.utils.DBUtils import get_email_address_by_address
from app.utils.DBUtils import get_email_id_by_mail_address

import pytest

def add_mail(client, email, password):
    return client.post(
    '/dashboard/add_email', data={
    'email_address' : email,
    'password' : password
    },
    follow_redirects=True
    )

def enable_disable_mail(client, mail_id):
    return client.get('/dashboard/emails/activation/{}'.format(mail_id), follow_redirects=True)

def enable_disable_notif(client, mail_id):
    return client.get('/dashboard/emails/notif/{}'.format(mail_id), follow_redirects=True)

def detection_check(client, mail_id):
    return client.get('/dashboard/emails/phish/{}'.format(mail_id), follow_redirects=True)

def detection_history(client, mail_id):
    return client.get('/dashboard/emails/history/{}'.format(mail_id), follow_redirects=True)

# Make sure user is valid and email does not exist in database
# Assert HTTP code, assert database entry, assert new mail displayed in page
def test_invalid_add_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    EMAIL_ADDR = 'testuser@test.com'
    EMAIL_PASSWORD = 'password'

    login(client, USERNAME, PASSWORD)
    response = add_mail(client, EMAIL_ADDR, EMAIL_PASSWORD)
    assert response.status_code == 200
    assert b'Unable to connect to mailbox.' in response.data

def test_invalid_add_mail_password(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = 'password'

    login(client, USERNAME, PASSWORD)
    response = add_mail(client, EMAIL_ADDR, EMAIL_PASSWORD)
    assert response.status_code == 200
    assert b'Unable to connect to mailbox.' in response.data

def test_valid_add_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]

    login(client, USERNAME, PASSWORD)
    response = add_mail(client, EMAIL_ADDR, EMAIL_PASSWORD)
    assert response.status_code == 200
    assert get_email_address_by_address(EMAIL_ADDR)
    assert b'piscator.fisherman@gmail.com' in response.data

def test_valid_add_existing_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]

    login(client, USERNAME, PASSWORD)
    response = add_mail(client, EMAIL_ADDR, EMAIL_PASSWORD)
    assert response.status_code == 200
    assert b'piscator.fisherman@gmail.com already exist in our database!' in response.data

def test_check_email(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    login(client, USERNAME, PASSWORD)
    mail_id = get_email_id_by_mail_address(EMAIL_ADDR)
    response = detection_check(client, mail_id)
    assert response.status_code == 200
    assert b'Detection Results' in response.data

def test_detection_history(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    login(client, USERNAME, PASSWORD)
    mail_id = get_email_id_by_mail_address(EMAIL_ADDR)
    response = detection_history(client, mail_id)
    assert response.status_code == 200
    assert b'Detection History' in response.data

def test_valid_disable_enable_mail(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    login(client, USERNAME, PASSWORD)
    mail_id = get_email_id_by_mail_address(EMAIL_ADDR)
    response = enable_disable_mail(client, mail_id)
    updated_status = get_email_address_by_address('piscator.fisherman@gmail.com').get_active_status()
    assert response.status_code == 200
    assert updated_status == False

    response = enable_disable_mail(client, mail_id)
    updated_status = get_email_address_by_address('piscator.fisherman@gmail.com').get_active_status()
    assert response.status_code == 200
    assert updated_status == True

def test_valid_disable_enable_daily_notif(client, db):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    login(client, USERNAME, PASSWORD)
    mail_id = get_email_id_by_mail_address(EMAIL_ADDR)
    response = enable_disable_notif(client, mail_id)
    updated_pref = get_email_address_by_address('piscator.fisherman@gmail.com').get_notification_pref()
    assert response.status_code == 200
    assert updated_pref == False

    response = enable_disable_notif(client, mail_id)
    updated_pref = get_email_address_by_address('piscator.fisherman@gmail.com').get_notification_pref()
    assert response.status_code == 200
    assert updated_pref == True
