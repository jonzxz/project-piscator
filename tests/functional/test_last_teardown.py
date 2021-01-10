import pytest
from app import db
from app.models.User import User
from app.models.EmailAddress import EmailAddress


def test_teardown():
    email = db.session.query(EmailAddress).filter(EmailAddress.email_address == 'piscator.fisherman@gmail.com').first()
    user = db.session.query(User).filter(User.username == 'testuser123').first()
    # disable_user = db.session.query(User).filter(User.username == 'iamdisabled').first()
    disable_user = db.session.query(User).filter(User.username == 'disableme').first()

    if email:
        db.session.delete(email)
    if user:
        db.session.delete(user)
    if disable_user:
        db.session.delete(disable_user)

    db.session.commit()
