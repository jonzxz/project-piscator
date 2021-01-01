from test_2_authentication import login
from app.models.EmailAddress import EmailAddress

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

# Make sure user is valid and email does not exist in database
# Assert HTTP code, assert database entry, assert new mail displayed in page
def test_valid_add_mail(client, db):
    login(client, 'testuser123', 'password')
    response = add_mail(client, 'testmail456@mymail.com', 'password')
    # db.session.commit()
    assert response.status_code == 200
    assert db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    assert b'testmail456@mymail.com' in response.data

def test_valid_disable_mail(client, db):
    login(client, 'testuser123', 'password')
    mail_address = EmailAddress.query.filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    mail_id = mail_address.get_email_id()
    response = enable_disable_mail(client, mail_id)
    updated_status = EmailAddress.query.filter(EmailAddress.email_address == 'testmail456@mymail.com').first().get_active_status()
    assert response.status_code == 200
    assert updated_status == False
