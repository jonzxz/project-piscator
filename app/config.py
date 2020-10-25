import os

class Config(object):
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "pa$$w0rd"
    POSTGRES_URL = "localhost"
    POSTGRES_DB = "fyp-20s4-06p"
    SECRET_KEY = 'secret'
    # uri_template = 'postgresql+psycopg2://{usr}:{pw}@{url}/{db}'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or uri_template.format(
    # usr=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB)
    #
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
