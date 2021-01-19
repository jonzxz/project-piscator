from flask_wtf import FlaskForm
from app.models import User
from wtforms import PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired

# WTForm for updating password after request for password reset
class UpdatePasswordForm(FlaskForm):
    token = DecimalField('Six Digit Code'\
    , render_kw={"placeholder" : "Six-digit code"}, validators=[DataRequired()])
    new_password = PasswordField('New Password'\
    , render_kw={"placeholder" : "New Password"}, validators=[DataRequired()])
    submit = SubmitField('Reset')
