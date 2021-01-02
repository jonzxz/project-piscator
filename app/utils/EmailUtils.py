## Email libraries
from app import logger, mailer
from imap_tools import MailBox
import imaplib
from app.utils.Constants import *
from datetime import datetime
from flask_mail import Message

def test_mailbox_conn(email_addr, password):
    try:
        logger.info("Connecting to mailbox..")
        mail_provider = get_imap_svr(email_addr)
        mailbox = MailBox(mail_provider)
        mailbox.login(email_addr, password)
        conn_status = True
        logger.info("Connection successful")
        mailbox.logout()
    except imaplib.IMAP4.error:
        conn_status = False
        logger.error("Attempting connection to mailbox failed!")
    return conn_status

def get_imap_svr(email_addr):
    mail_provider = email_addr.split(sep='@')[1]
    if 'gmail' in mail_provider:
        return IMAP_GMAIL
    if 'hotmail' in mail_provider or 'live' in mail_provider or 'outlook' in mail_provider:
        return IMAP_OUTLOOK
    # more imap servers to be added - test mailbox conn first before adding in here

# Will not work if TESTING is True
def send_contact_us_email(email, msg_body):
    logger.info("Entering send_email")
    # logger.debug("USERNAME %s", username)
    msg = Message("Mail from {}".format(email), recipients=['piscator.fisherman@gmail.com'])
    msg.body = "Message from: {}\nDate sent:{}\nContent:{}".format(
    email, datetime.now(), msg_body)
    mailer.send(msg)
    logger.info("Email sent")

# Will not work if TESTING is True
def send_phish_check_notice(destination, phishing_mails):
    logger.info("Entering send_phish_check_notice")
    msg = Message("Piscator: Phishing Check Completed for {} on {}" \
    .format(destination, datetime.now().strftime("%d-%m-%Y, %H:%M"))\
    , recipients = [destination])

    msg.body = "You have recently requested for a phishing check on {}\n".format(destination)
    msg.body += "These are the phishing emails detected - \n\n"

    for phish_mail in phishing_mails:
        msg.body += phish_mail.__repr__() + '\n\n'
    mailer.send(msg)
    logger.info("Phish check notice sent.")

def send_password_token(destination, username, token):
    logger.info("Entering send_password_token")
    msg = Message("You have recently requested a password reset for your account on Project Piscator." \
    , recipients=[destination])

    msg.body = "Hi {}, you have recently requested a password reset for your account on Project Piscator.\n".format(username)
    msg.body += "The token generated for your password reset is {}. This token will be valid for 1 hour(s).\n".format(token)
    msg.body += "If you did not request for this password reset, please contact the administrative team immediately.\n"
    mailer.send(msg)
    logger.info("Password reset token email sent")
