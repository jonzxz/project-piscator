## Application Objects
from app import db

## Authentication Utilities
from app import login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

## Utilities
from datetime import datetime
from random import randint

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
    reset_token = db.Column(db.Numeric(6, 0), unique=True, nullable=True)

    def __repr__(self) -> str:
        return "User ID: {} -- Username: {}".format(self.user_id, self.username)

    def get_id(self) -> int:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def get_active_status(self) -> bool:
        return self.is_active

    def set_active_status(self, boolean: bool) -> None:
        self.is_active = boolean

    def get_admin_status(self) -> bool:
        return self.is_admin == True

    def set_admin_status(self, boolean: bool) -> None:
        self.is_admin = boolean

    def get_created_at(self) -> datetime:
        return self.created_at

    def set_created_at(self, created_at: datetime) -> None:
        self.created_at = created_at

    def get_last_logged_in(self) -> datetime:
        return self.last_logged_in

    def set_last_logged_in(self, last_logged: datetime) -> None:
        self.last_logged_in = last_logged

    def generate_reset_token(self) -> None:
        self.reset_token = randint(100000, 999999)

    def get_reset_token(self) -> int:
        return self.reset_token

    def delete_reset_token(self) -> None:
        self.reset_token = None

    @login.user_loader
    def load_user(id: int):
        return User.query.get(int(id))
