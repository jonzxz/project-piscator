from app import db
from app.models.User import User
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
# from wtforms import StringField
# from flask_admin.form.upload import ImageUploadField
# from wtforms.validators import DataRequired, NumberRange, ValidationError, Email
# from app.forms.custom_validators import Interval, DateInRange
# from app.views import utils, filters
from flask_login import current_user
from flask import redirect, url_for
# from sqlalchemy.sql import func
# from datetime import date, timedelta
# from pathlib import Path
# from os import path
# import math

class GlobalIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))
