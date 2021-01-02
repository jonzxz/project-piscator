import os
from app.utils.FileUtils import get_recaptcha_secret
from app.utils.FileUtils import get_server_mail_cred

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
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET') or get_recaptcha_secret()
    RECAPTCHA_OPTIONS = {'theme' : 'black'}

    # Configures ReCAPTCHA and Contact Us
    # If TESTING = True, ReCAPTCHA will be inactive and Flask-Mail Contact us will NOT work
    # If TESTING = False, ReCAPTCHA will be active and Flask-Mail Contact us will work
    TESTING=os.environ.get('TESTING') or False

    # Flask-Mail Configs
    MAIL_CREDS = get_server_mail_cred()
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_ADDR') or MAIL_CREDS[0]
    MAIL_PASSWORD = os.environ.get('MAIL_PASS') or MAIL_CREDS[1]
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_ADDR') or MAIL_CREDS[0]
    MAIL_USE_TSL = False
    MAIL_USE_SSL = True
    MAIL_SUPRRESS_SEND = False
