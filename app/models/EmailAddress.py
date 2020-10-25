from app import db
from datetime import datetime

# Defines model for EmailAddress class
class EmailAddress(db.Model):
    __tablename__ = 'email_address'
    email_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return "Email Address: {} -- Owned by User ID: {}".format(self.email_address, self.user_id)
