import os
from app.utils.RecaptchaUtils import get_recaptcha_secret

class Config(object):
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "pa$$w0rd"
    POSTGRES_URL = "localhost"
    POSTGRES_DB = "fyp-20s4-06p"
    SECRET_KEY = 'secret'
    uri_template = 'postgresql+psycopg2://{usr}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or uri_template.format(
    usr=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB)

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Recaptcha
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6Lezk-IZAAAAABW4o03l4BBW8OpmmZ8p7GhUZQC0'
    RECAPTCHA_PRIVATE_KEY = get_recaptcha_secret()
    RECAPTCHA_OPTIONS = {'theme' : 'black'}
