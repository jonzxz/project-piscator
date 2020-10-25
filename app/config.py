import os

class Config(object):
    SECRET_KEY = 'secret'
    uri_template = 'postgresql+psycopg2://{usr}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or uri_template.format(usr="postgres", pw="pa$$w0rd", url="localhost", db="fyp-20s4-06p")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
