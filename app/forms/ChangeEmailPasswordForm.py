from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

# WTForm for "Change Password" in Subscribers' Dashboard for email address
class ChangeEmailPasswordForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password: ', render_kw={"placeholder": "New Password"})
    change_email_password_submit = SubmitField('Update')
