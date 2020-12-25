from app import db
from app.models.User import User
from app.models.EmailAddress import EmailAddress

def get_user_by_id(id):
    return db.session.query(User).filter(User.user_id == id).first()

def get_user_by_name(username):
    return db.session.query(User).filter(User.username == username).first()

def get_email_address_by_address(mail_address):
    return db.session.query(EmailAddress).filter(EmailAddress.email_address == mail_address).first()

def get_email_address_by_email_id(mail_id):
    return db.session.query(EmailAddress).filter(EmailAddress.email_id == mail_id).first()

def get_existing_addresses_by_user_id(id):
    return db.session.query(EmailAddress).filter(EmailAddress.user_id == id).all()

def get_owner_id_from_email_id(mail_id):
    return db.session.query(EmailAddress) \
            .filter(EmailAddress.email_id == mail_id) \
            .first() \
            .get_user_id()
