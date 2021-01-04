import pytest
from app import db
from app.models.User import User
from app.models.EmailAddress import EmailAddress


def test_teardown():
    email = db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    user = db.session.query(User).filter(User.username == 'testuser123').first()
    disable_user = db.session.query(User).filter(User.username == 'disableme').first()
    reset_user = db.session.query(User).filter(User.username == 'resetmyaccount').first()
    reset_email = db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail789@mymail.com').first()
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
