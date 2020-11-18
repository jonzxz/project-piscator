from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[DataRequired(), Email()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Contact Us')
