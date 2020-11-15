## Email libraries
from app import logger
from imap_tools import MailBox
import imaplib

def test_mailbox_conn(email_addr, password):
    try:
        logger.info("Connecting to mailbox..")
        mail_provider = 'imap.gmail.com'
        mailbox = MailBox(mail_provider)
        mailbox.login(email_addr, password)
        conn_status = True
        logger.info("Connection successful")
        mailbox.logout()
    except imaplib.IMAP4.error:
        conn_status = False
        logger.error("Attempting connection to mailbox failed!")
    return conn_status
