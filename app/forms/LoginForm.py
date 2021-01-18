from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

# WTForm for Login page
class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}\
    , validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}\
    , validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
