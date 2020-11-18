from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
import logging


# Application instance and application config instance
app = Flask(__name__)
app.config.from_object(Config)


# Database instance
db = SQLAlchemy(app)

# Encryption
from app.utils.Encryption import Encryption

encryption_engine = Encryption()

# Migration engine instance
# Whenever database has updates on schema
# do a flask db migrate -m "COMMIT_MSG"
# to generate a script that will execute the changes
# do a flask db upgrade
# to update the database
# if you messed up, do a flask db downgrade
migrate = Migrate(app, db)

# Flask Login
login = LoginManager(app)

# Logger
logger = logging.getLogger(__name__)
# Root debug level
logger.setLevel(level=logging.DEBUG)
# CLI Debug Handler config - set to DEBUG and above.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_formatter = logging.Formatter('[LOG] [%(levelname)s] [%(funcName)s:%(lineno)s] : %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


# File Debug Handler Config - set to WARNING and above only.
file_handler = logging.FileHandler('app_logs.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('[LOG] [%(levelname)s] [%(asctime)s] [%(funcName)s:%(lineno)s] : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Flask Mail
from flask_mail import Mail
mailer = Mail(app)

from app import routes
# Add all new models here
from app.models import User, EmailAddress, PhishingEmail


from app.views import views

# Admin instance
admin = Admin(app, name='piscator', template_mode='bootstrap4', index_view=views.GlobalIndexView())
