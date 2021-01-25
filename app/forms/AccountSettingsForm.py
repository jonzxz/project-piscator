from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo

# WTForm for "Account Settings" in Subscribers' Dashboard
class AccountSettingsForm(FlaskForm):
	username = StringField('Username: ')
	current_password = PasswordField('Current Password: '\
	, render_kw={"placeholder": "Current Password"}\
	, validators=[DataRequired(message='Please enter your \'Current Password\'!')])

	new_password = PasswordField('New Password: '\
	, render_kw={"placeholder": "New Password"}\
	, validators=[DataRequired(message='Password cannot be empty!')])

	confirm_new_password = PasswordField('Confirm New Password: '\
	, render_kw={"placeholder": "Confirm New Password"}\
	, validators=[
		EqualTo('new_password'\
		, message='New Password and Confirm New Password must match!')
		, DataRequired(message='Confirm Password cannot be empty!')
		])

	update_password_submit = SubmitField('Update')
