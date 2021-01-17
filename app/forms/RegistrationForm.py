from flask_wtf import FlaskForm, RecaptchaField
from app.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

# WTForm for Registration page
class RegistrationForm(FlaskForm):
	username = StringField('Username', render_kw={"placeholder": "Username"}\
	, validators=[DataRequired()])
	password = PasswordField('Password', render_kw={"placeholder": "Password"}\
	, validators=[DataRequired()])

	confirm_password = PasswordField('Confirm Password'\
	, render_kw={"placeholder": "Confirm Password"}, validators=[DataRequired()\
	, EqualTo('password', message='Password must match!')])

	agreement = BooleanField('Agreement', validators=[DataRequired(\
	message='You must agree to the terms and policies to register!')])

	recaptcha = RecaptchaField()
	submit = SubmitField('Register')
