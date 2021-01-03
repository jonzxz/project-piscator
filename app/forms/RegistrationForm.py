from flask_wtf import FlaskForm, RecaptchaField
from app.models import User
from wtforms import FormField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
	#email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm Password"},
		validators=[DataRequired(),
					EqualTo('password', message='Password must match!')])
	agreement = BooleanField('Agreement', validators=[DataRequired(message='You must agree to the terms and policies to register!')])
	recaptcha = RecaptchaField()
	submit = SubmitField('Register')

	# def validate_username(self, username):
	# 	user = User.query.filter_by(username=username.data).first()
	# 	if user is not None:
	# 		raise ValidationError('Username already taken')

	# def validate_email(self, email):
	# 	user = User.query.filter_by(email=email.data).first()
	# 	if user is not None:
	# 		raise ValidationError('Email already taken')
