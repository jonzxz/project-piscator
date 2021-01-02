from flask_wtf import FlaskForm
from app.models import User
from wtforms import FormField, StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError, Email

class ResetPasswordForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    email_address = EmailField('Email Address', render_kw={"placeholder": "Email Address"} \
    , validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')
