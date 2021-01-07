from flask_wtf import FlaskForm
from wtforms import FormField, StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

class AddEmailForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Email Address Password', validators=[DataRequired()])
    add_mail_submit = SubmitField('Add Email')
