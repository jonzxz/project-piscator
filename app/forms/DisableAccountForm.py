from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo

# WTForm for "Disable Account" in Subscribers' Dashboard
class DisableAccountForm(FlaskForm):
	username = StringField('Username: ')
	current_password = PasswordField('Current Password: '\
	, render_kw={"placeholder": "Current Password"}\
	, validators=[DataRequired(message='Please enter your \'Current Password\'!')])

	disable_account = BooleanField('Disable Account: ')
	disable_acc_submit = SubmitField('Update')
