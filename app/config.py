import os

class Config(object):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://localhost/fyp-20s4-06p'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
