import sys, os

def get_recaptcha_secret() -> str:
    try:
        with open('RECAPTCHA_SECRET.key', 'r') as secret:
            key = secret.read()
            secret.close()
            return key
    except FileNotFoundError as fnfe:
        print("ReCAPTCHA secret key file not found! Loading from ENV")
        return os.environ.get('RECAPTCHA_SECRET')

def get_server_mail_cred():
    try:
        with open('MAIL_CRED.key', 'r') as mail_cred:
            creds = mail_cred.read().split(sep='\n')
            mail_cred.close()
            return creds
    except FileNotFoundError as fnfe:
        print("MAIL_CRED key file not found! Loading from ENV")
        return [os.environ.get('MAIL_ADDR'), os.environ.get('MAIL_PASS')]
