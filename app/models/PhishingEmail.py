from app import db
from datetime import datetime
from sqlalchemy import extract
from sqlalchemy.ext.hybrid import hybrid_property

# Defines model for EmailAddress class
class PhishingEmail(db.Model):
    __tablename__ = 'phishing_email'
    mail_id = db.Column(db.Integer, primary_key=True)
    sender_address = db.Column(db.String(255), index=True, unique=False, nullable=False)
    subject = db.Column(db.Text, nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    receiver_id = db.Column(db.Integer, db.ForeignKey('email_address.email_id'), index=True, unique=False, nullable=False)

    def __repr__(self):
        return "From: {}\nSubject: {}".format(self.sender_address, self.subject)
        # return "Received by: {} -- Month Created: {}".format(self.receiver_id, self.get_created_month())

    def get_sender_address(self):
        return self.sender_address

    def get_subject(self):
        return self.subject

    def get_detected_on(self):
        return self.created_at

    def get_created_month(self):
        return self.created_at.month

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
