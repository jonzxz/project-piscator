from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate

# Application instance and application config instance
app = Flask(__name__)
app.config.from_object(Config)

# Database instance
db = SQLAlchemy(app)

# Migration engine instance
# Whenever database has updates on schema
migrate = Migrate(app, db)

from app import routes, models
