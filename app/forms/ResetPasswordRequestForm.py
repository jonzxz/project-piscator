from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

# WTForm for requesting a Password Reset
class ResetPasswordRequestForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    email_address = EmailField('Email Address', render_kw={"placeholder": "Email Address"} \
    , validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')
