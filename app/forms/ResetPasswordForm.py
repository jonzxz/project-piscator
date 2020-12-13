from flask_wtf import FlaskForm
from app.models import User
from wtforms import FormField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class ResetPasswordForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    submit = SubmitField('Reset')
