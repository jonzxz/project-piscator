from flask_wtf import FlaskForm
from app.models import User
from wtforms import FormField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
