from app import db, logger
from app.models.User import User
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField
# from flask_admin.form.upload import ImageUploadField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Email
# from app.forms.custom_validators import Interval, DateInRange
# from app.views import utils, filters
from flask_login import current_user
from flask import redirect, url_for
# from sqlalchemy.sql import func
# from datetime import date, timedelta
# from pathlib import Path
# from os import path
# import math
from werkzeug.security import generate_password_hash

class GlobalIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

class BaseView(ModelView):
	# pass
	def scaffold_filters(self, name):
		filters = super().scaffold_filters(name)
		if hasattr(self, 'column_filter_labels') and name in self.column_filter_labels:
			for f in filters:
				f.name = self.column_filter_labels[name]
		return filters

class AdminBaseView(BaseView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

## User table view
class AdminUserView(AdminBaseView):
	### Display Rules
	# Page set allowed
	# PK displayed, selected columns relabelled and displayed
	can_set_page_size = True
	column_display_pk = True
	column_list = ['user_id', 'username', 'created_at', 'last_logged_in', 'is_active', 'is_admin']
	column_labels = {
		'user_id' : 'ID',
		'created_at' : 'Created At',
		'last_logged_in' : 'Last Logged In',
		'is_admin' : 'Admin',
		'is_active' : 'Active'
	}

	## Custom View template
	list_template = 'admin/admin_base_list.html'
	create_template = 'admin/admin_base_create.html'
	edit_template = 'admin/admin_base_edit.html'

	# Sortable columns
	column_sortable_list = ['user_id', 'username', 'created_at', 'last_logged_in', 'is_active', 'is_admin']

	### Create / Edit form rules
	# Additional fields not in column_list
	# 'password' for creating new users
	# 'change_password' for editing existing users
	form_extra_fields = {
		'password' : StringField('Password', validators=[DataRequired()]),
		'change_password': StringField('Change Password') }

	# Changes created_at and last_logged_in to be unmodifiable when editing entity
	form_widget_args = {
		'created_at' : {
			'readonly' : True,
			'disabled' : True
		},
		'last_logged_in' : {
			'readonly' : True,
			'disabled' : True
		},
	}

	# Rulesets for creating and editing, these columns will appear in respective pages (create / edit)
	form_create_rules = ['username', 'password', 'is_admin']
	form_edit_rules = ['username', 'change_password', 'created_at', 'last_logged_in', 'is_active', 'is_admin']

	# Function on creating a new user or editing password of user
	def on_model_change(self, form, model, is_created):
		logger.info("User form submitted")
		# If new user is created
		if is_created:
			logger.info("New user created: {}".format(model.get_username()))
			model.set_password(form.password.data)
		else:
			# If change_password field has data. If edit and field is empty does not do anything
			if form.change_password.data:
				logger.info("User {}'s password is changed".format(model.get_username()))
				# Password hashing is automatically done on Model level
				model.set_password(form.change_password.data)

	# Function on deleting user - handling of deleting currently logged in user
	def on_model_delete(self, model):
		if model == current_user:
			logger.error("Attempted to delete {} as {}. Throwing error".format(model.get_username(), current_user.get_username()))
			raise ValidationError('Cannot delete currently logged in account')

	# Function to prefill edit forms - called when edit_view is invoked
	# During editing of entries, the username is set to readonly so it cannot be modified
	def on_form_prefill(self, form, model):
		form.username.render_kw = {
			'readonly':True
		}

class AdminEmailView(AdminBaseView):
	### Display Rules
	# Page set allowed
	# PK displayed, selected columns relabelled and displayed
	can_set_page_size = True
	column_display_pk = True
	column_list = ['email_id', 'email_address', 'user_id', 'last_mailbox_size', 'phishing_mail_detected', 'created_at', 'last_updated', 'active']
	column_labels = {
		'email_id' : 'ID',
		'email_address' : 'Email Address',
		'user_id' : 'Owner ID',
		'last_mailbox_size' : 'Last Mailbox Size',
		'phishing_mail_detected' : 'Detection Count',
		'created_at' : 'Created At',
		'last_updated' : 'Last Updated'
	}

	list_template = 'admin/admin_base_list.html'
	create_template = 'admin/admin_base_create.html'
	edit_template = 'admin/admin_base_edit.html'
	# Sortable columns
	columns_sortable_list = ['email_id', 'user_id', 'phishing_mail_detected', 'created_at', 'last_updated']

	### Create / Edit form rules
	# Additional fields not in column_list
	# 'email_password' for creating new addresses
	# 'change_password' for editing existing addresses
	form_extra_fields = {
		'email_password' : StringField('Password', validators=[DataRequired()]),
		'change_password': StringField('Change Password')
	}

	# Read only columns for the following supposedly manually unmodifiable columns
	form_widget_args = {
		'last_mailbox_size' : {
			'readonly' : True,
			'disabled' : True
		},
		'phishing_mail_detected' : {
			'readonly' : True,
			'disabled' : True
		},
		'created_at' : {
			'readonly' : True,
			'disabled' : True
		},
		'last_updated' : {
			'readonly' : True,
			'disabled' : True
		}
	}

	# Rulesets for creating and editing, these columns will appear in respective pages (create / edit)
	form_create_rules = ['email_address', 'email_password', 'user']
	form_edit_rules = ['email_address', 'change_password', 'user', 'last_mailbox_size', 'phishing_mail_detected', 'created_at', 'last_updated', 'active' ]

	# Function on creating a new address or editing password of an address
	def on_model_change(self, form, model, is_created):
		logger.info("Email form submitted")
		# If new email is created
		if is_created:
			logger.info("New email created: {}".format(model.get_email_address()))
			model.set_email_password(form.email_password.data)
		else:
			if form.change_password.data:
				logger.info("Email Addr {}'s password is changed".format(model.get_email_address()))
				model.set_email_password(form.change_password.data)

	# Function to prefill edit forms - called when edit_view is invoked
	# During editing of entries, the email is set to readonly so it cannot be modified
	def on_form_prefill(self, form, model):
		form.email_address.render_kw = {
			'readonly':True
		}
