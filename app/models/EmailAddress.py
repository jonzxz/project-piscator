## Application Objects
from app import db, encryption_engine

## Utilities
from datetime import datetime

# Defines model for EmailAddress class
class EmailAddress(db.Model):
    __tablename__ = 'email_address'
    email_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), index=True, unique=True\
    , nullable=False)
    email_password = db.Column(db.String(255), nullable=False)
    phishing_mail_detected = db.Column(db.Integer, nullable=True, default=0)
    total_mails_checked = db.Column(db.Integer, nullable=True, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    last_updated = db.Column(db.DateTime, nullable=True, default=None)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    owner = db.relationship('User', backref='addresses')
    phishing_mails = db.relationship('PhishingEmail', backref='owner'\
    , lazy='dynamic')

    def __repr__(self):
        return "Email Address: {} -- Owned by User ID: {}"\
        .format(self.email_address, self.owner_id)

    def get_email_id(self) -> int:
        return self.email_id

    def get_email_address(self) -> str:
        return self.email_address

    def set_email_address(self, email_addr: str) -> None:
        self.email_address = email_addr

    def get_email_password(self) -> str:
        return self.email_password

    def set_email_password(self, pw: str) -> None:
        self.email_password = encryption_engine.encrypt(pw)

    def get_decrypted_email_password(self) ->str:
        return encryption_engine.decrypt(self.email_password)

    def set_owner_id(self, user_id: int):
        self.owner_id = user_id

    def get_owner_id(self) -> int:
        return self.owner_id

    def set_mailbox_size(self, last_mb_size: int):
        self.last_mailbox_size = last_mb_size

    def get_mailbox_size(self) -> int:
        return self.last_mailbox_size

    def set_phishing_mail_detected(self, num_phish_detected: int):
        self.phishing_mail_detected += num_phish_detected

    def get_phishing_mail_detected(self) -> int:
        return self.phishing_mail_detected

    def get_active_status(self) -> bool:
        return self.active

    def set_active_status(self, boolean: bool):
        self.active = boolean

    def get_active_status(self) -> bool:
        return self.active

    def set_created_at(self, created_at: datetime):
        self.created_at = created_at

    def get_created_at(self) -> datetime:
        return self.created_at

    def set_last_updated(self, last_updated: datetime):
        self.last_updated = last_updated

    def get_last_updated(self) -> datetime:
        return self.last_updated


    def get_prettified_date(self) -> str:
        return self.get_last_updated().strftime('%d-%m-%Y %H:%M')
