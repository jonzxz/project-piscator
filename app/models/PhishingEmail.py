## Application Objects
from app import db

## Utilities
from datetime import datetime
from sqlalchemy import extract
from sqlalchemy.ext.hybrid import hybrid_property

# Defines model for EmailAddress class
class PhishingEmail(db.Model):
    __tablename__ = 'phishing_email'
    mail_id = db.Column(db.Integer, primary_key=True)
    sender_address = db.Column(db.String(255), index=True, unique=False\
    , nullable=False)
    subject = db.Column(db.Text, nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    receiver_id = db.Column(db.Integer, db.ForeignKey('email_address.email_id')\
    , index=True, unique=False, nullable=False)

    def __repr__(self) -> str:
        return "From: {}\nSubject: {}".format(self.sender_address, self.subject)

    def get_sender_address(self) -> str:
        return self.sender_address

    def get_subject(self) -> str:
        return self.subject

    def get_detected_on(self) -> datetime:
        return self.created_at

    def get_created_month(self) -> int:
        return self.created_at.month

    """
    Following hybrid properties are created to retrieve phishing emails detected
    based on the time criteria for monthly overview in dashboard statistics
    """
    @hybrid_property
    def created_at_year(self):
        return self.created_at.year

    @created_at_year.expression
    def created_at_year(cls):
        return extract('year', cls.created_at)

    @hybrid_property
    def created_at_month(self):
        return self.created_at.month

    @created_at_month.expression
    def created_at_month(cls):
        return extract('month', cls.created_at)

    @hybrid_property
    def created_at_week(self):
        return self.created_at.isocalendar()[1]

    @created_at_week.expression
    def created_at_week(cls):
        return extract('week', cls.created_at)
