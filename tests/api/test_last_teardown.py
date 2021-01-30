import pytest
from app import db
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.utils.FileUtils import get_server_mail_cred

# Teardown function to remove all records created during test cases
def test_teardown():
    MAIL_CREDS = get_server_mail_cred()

    email = db.session.query(EmailAddress)\
    .filter(EmailAddress.email_address == MAIL_CREDS[0])\
    .first()

    user = db.session.query(User).filter(User.username == 'testuser123')\
    .first()

    disable_user = db.session.query(User).filter(User.username == 'disableme')\
    .first()

    reset_user = db.session.query(User).filter(User.username == 'resetmyaccount')\
    .first()

    reset_email = db.session.query(EmailAddress)\
    .filter(EmailAddress.email_address == MAIL_CREDS[2])\
    .first()

    if email:
        db.session.delete(email)
    if user:
        db.session.delete(user)
    if disable_user:
        db.session.delete(disable_user)
    if reset_user:
        db.session.delete(reset_user)
    if reset_email:
        db.session.delete(reset_email)

    db.session.commit()
