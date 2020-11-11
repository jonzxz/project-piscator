from app import db
from datetime import datetime

# Defines model for EmailAddress class
class EmailAddress(db.Model):
    __tablename__ = 'email_address'
    email_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email_password = db.Column(db.String(255), nullable=False)
    last_mailbox_size = db.Column(db.Integer, nullable=True, default=None)
    phishing_mail_detected = db.Column(db.Integer, nullable=True, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    last_updated = db.Column(db.DateTime, nullable=True, default=None)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    phishing_mails = db.relationship('PhishingEmail', backref='owner', lazy='dynamic')

    def __repr__(self):
        return "Email Address: {} -- Owned by User ID: {}".format(self.email_address, self.user_id)

    def set_email_password(self, encrypted_pw: str):
        self.email_password = encrypted_pw

    def get_email_password(self) -> str:
        return self.email_password

    def set_mailbox_size(self, last_mb_size: int):
        self.last_mailbox_size = last_mb_size

    def get_mailbox_size(self) -> int:
        return self.last_mailbox_size

    def set_phishing_mail_detected(self, num_phish_detected: int):
        self.phishing_mail_detected = num_phish_detected

    def get_phishing_mail_detected(self) -> int:
        return self.phishing_mail_detected

    def get_active_status(self) -> bool:
        return self.active

    def set_active_status(self, boolean: bool):
        self.active = boolean

    def get_active_status(self) -> bool:
        return self.active

    def set_last_updated(self, last_updated: datetime):
        self.last_updated = last_updated

    def get_last_updated(self) -> datetime:
        return self.last_updated
