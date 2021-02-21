from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

# WTForm for "Add Email" modal in Subscribers' Dashboard
class AddEmailForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Application Password', validators=[DataRequired()])
    add_mail_submit = SubmitField('Add Email')
