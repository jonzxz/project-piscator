from flask_wtf import FlaskForm
from app.models import User
from wtforms import FormField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo

class AccountSettingsForm(FlaskForm):
	username = StringField('Username: ')
	current_password = PasswordField('Current Password: ', render_kw={"placeholder": "Current Password"}, validators=[DataRequired()])
	new_password = PasswordField('New Password: ', render_kw={"placeholder": "New Password"}, validators=[DataRequired()])
	confirm_new_password = PasswordField('Confirm New Password: ', render_kw={"placeholder": "Confirm New Password"},
		validators=[DataRequired(),
					EqualTo('new_password', message='Password must match!')])
	submit = SubmitField('Update')
