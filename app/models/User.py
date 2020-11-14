from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login

# Defines the model for User class
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    last_logged_in = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # FK
    emails = db.relationship('EmailAddress', backref='owner', lazy='dynamic')

    def __repr__(self):
        return "User ID: {} -- Username: {}".format(self.user_id, self.username)

    def get_id(self):
        return self.user_id

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    def update_active_status(self, boolean: bool):
        self.active = boolean

    def update_admin_status(self, boolean: bool):
        self.is_admin = boolean

    def get_active_status(self) -> bool:
        return self.is_active

    def get_admin_status(self) -> bool:
        return self.is_admin == True

    def get_username(self) -> str:
        return self.username

    def set_last_logged_in(self, last_logged: datetime):
        self.last_logged_in = last_logged

    def get_last_logged_in(self) -> datetime:
        return self.last_logged_in

    @login.user_loader
    def load_user(id: int):
        return User.query.get(int(id))
