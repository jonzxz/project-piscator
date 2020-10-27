from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

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
        return "User ID: {} -- Username: {}".format(self.user_id, self.username)

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
