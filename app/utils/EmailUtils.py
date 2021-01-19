## Application objects
from app import logger, mailer, db
from app.utils.Constants import *

## IMAP, Email libraries
from imap_tools import MailBox
import imaplib
from flask_mail import Message

## Date utilities
from datetime import datetime, date
from sqlalchemy import Date, cast

## Models
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Typehints
from typing import List

##
from socket import gaierror

"""
Function to test connection via IMAP, returns connection attempt results
"""
def test_mailbox_conn(email_addr: str, password: str) -> bool:
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
        logger.error("IMAP4 Error: Connection failed!")
    except gaierror:
        conn_status = False
        logger.error("GAIError: Connection failed")
    return conn_status

"""
Function to retrieve IMAP server based on email address
"""
def get_imap_svr(email_addr: str) -> str:
    mail_provider = email_addr.split(sep='@')[1]
    if 'gmail' in mail_provider:
        return IMAP_GMAIL
    if 'hotmail' in mail_provider or 'live' in mail_provider \
    or 'outlook' in mail_provider:
        return IMAP_OUTLOOK
    return 'INVALID'

"""
Will not work if TESTING is True
Function to send an email to project email, executed when "Contact Us" in
homepage is triggered
"""
def send_contact_us_email(email: str, msg_body: str) -> None:
    logger.info("Entering send_contact_us_email")
    msg = Message("Mail from {}".format(email) \
    , recipients=['piscator.fisherman@gmail.com'])
    msg.body = "Message from: {}\nDate sent:{}\nContent:{}".format(
    email, datetime.now(), msg_body)
    mailer.send(msg)
    logger.info("Email sent")

"""
Will not work if TESTING is True
Function to send an email to address that triggered a manual phishing check
"""
def send_phish_check_notice(destination: str \
, phishing_mails: List[PhishingEmail]) -> None:
    logger.info("Entering send_phish_check_notice")
    msg = Message("Piscator: Phishing Check Completed for {} on {}" \
    .format(destination, datetime.now().strftime("%d-%m-%Y, %H:%M"))\
    , recipients = [destination])

    msg.body = "You have recently requested for a phishing check on {}\n" \
    .format(destination)

    if len(phishing_mails) >= 1:
        msg.body += "These are the phishing emails detected - \n\n"

        for phish_mail in phishing_mails:
            msg.body += phish_mail.__repr__() + '\n\n'
    else:
        msg.body += "No phishing emails detected, congratulations!\n\n"

    msg.body +="This is an automated email sent from Project Piscator. "\
    "If you are not the intended recipient, please contact the administrative "\
    "team immediately."

    mailer.send(msg)
    logger.info("Phish check notice sent.")

"""
Will not work if TESTING is True
Function to send an email containing a password reset token upon reset request
"""
def send_password_token(destination: str, username: str, token: str) -> None:
    logger.info("Entering send_password_token")
    msg = Message("You have recently requested a password reset for your account"\
    " on Project Piscator.", recipients=[destination])

    msg.body = "Hi {}, you have recently requested a password reset for your "\
    "account on Project Piscator.\nThe token generated for your password reset "\
    "is {}. This token will be valid for 1 hour(s)\n If you did not request for "\
    "this password reset, please contact the administrative team immediately.\n"\
    .format(username, token)
    mailer.send(msg)
    logger.info("Password reset token email sent")

"""
Will not work if TESTING is True
Function to send an email if phishing emails are detected in an active mailbox
on a daily basis. Mails will not be sent if no phishing emails detected for
the day.
"""
def send_daily_notice() -> None:
    logger.info("Routine task: sending daily notice to all active mailboxes")

    all_active_mailboxes = db.session.query(EmailAddress)\
    .filter(EmailAddress.active == True).all()

    for mailbox in all_active_mailboxes:
        logger.info("Checking through %s if any phishing emails detected today.."\
        , mailbox.get_email_address())

        phishing_mail_detected_today = db.session.query(PhishingEmail)\
        .filter(PhishingEmail.receiver_id == mailbox.get_email_id()\
        , (cast(PhishingEmail.created_at, Date)) == date.today()).all()

        if phishing_mail_detected_today:
            logger.info("Populating message content with mails detected today [%s]"\
            " for %s..", date.today().strftime('%d/%m/%y')\
            , mailbox.get_email_address())

            msg = Message("Piscator: Daily Update on your mailbox {}"\
            .format(mailbox.get_email_address()) \
            , recipients =[mailbox.get_email_address()])

            msg.body = "Hi, this is your daily update from Project Piscator.\n\n"\
            " We have detected the following possible phishing emails in your inbox:\n\n"

            for mail_detected in phishing_mail_detected_today:
                msg.body += mail_detected.__repr__() + '\n\n'
            mailer.send(msg)
            logger.info("Daily notice email sent for %s"\
            , mailbox.get_email_address())
        else:
            logger.info("No phishing emails detected today [%s] for %s"\
            , date.today().strftime('%d/%m/%y'), mailbox.get_email_address())
