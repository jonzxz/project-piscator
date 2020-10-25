from app import db
from datetime import datetime

# Defines the model for User class
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)

    # FK
    emails = db.relationship('EmailAddress', backref='owner', lazy='dynamic')

    def __repr__(self):
        return "User ID: {} -- Username: {}".format(self.user_id, self_username)

    def get_id(self):
        return self.user_id
