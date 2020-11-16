## Email libraries
from app import logger
from imap_tools import MailBox
import imaplib

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
        return 'imap.gmail.com'
    if 'hotmail' in mail_provider or 'live' in mail_provider or 'outlook' in mail_provider:
        return 'outlook.office365.com'
    # if hotmail / live in mail provider return outlook imap svr
