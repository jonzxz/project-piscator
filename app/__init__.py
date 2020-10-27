from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
#from flask_heroku import Heroku

# Application instance and application config instance
app = Flask(__name__)
app.config.from_object(Config)

# Database instance
db = SQLAlchemy(app)
#heroku = Heroku(app)

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

from app import routes
# Add all new models here
from app.models import User, EmailAddress
