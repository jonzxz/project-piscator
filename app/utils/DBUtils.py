## Application objects
from app import db, logger, model

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail
from app.models.Mail import Mail
from app.machine_learning.EmailData import EmailData

## Email Utilities
from app.utils.EmailUtils import send_phish_check_notice
from app.utils.EmailUtils import get_imap_svr

## IMAP, email libraries
from email.errors import HeaderParseError
from imap_tools import MailBox, AND, OR

# Date utilities
from datetime import datetime, date

## Typehints
from typing import List

"""
Function to retrieve User based on id
"""
def get_user_by_id(id: int) -> User:
    return db.session.query(User).filter(User.user_id == id).first()

"""
Function to retrieve User based on username
"""
def get_user_by_name(username: str) -> User:
    return db.session.query(User).filter(User.username == username).first()

"""
Function to retrieve EmailAddress based on email_address
"""
def get_email_address_by_address(mail_address: str) -> EmailAddress:
    return db.session.query(EmailAddress)\
            .filter(EmailAddress.email_address == mail_address)\
            .first()

"""
Function to retrieve EmailAddress based on email_id
"""
def get_email_address_by_email_id(mail_id: int) -> EmailAddress:
    return db.session.query(EmailAddress)\
            .filter(EmailAddress.email_id == mail_id)\
            .first()

"""
Function to retrieve ID for EmailAddress based on email_address
"""
def get_email_id_by_mail_address(mail_address: str) -> int:
    return db.session.query(EmailAddress) \
            .filter(EmailAddress.email_address == mail_address) \
            .first() \
            .get_email_id()

"""
Function to retrieve list of EmailAddress based on User ID
"""
def get_existing_addresses_by_user_id(id: int) -> List[EmailAddress]:
    return db.session.query(EmailAddress)\
            .filter(EmailAddress.owner_id == id)\
            .all()

"""
Function to retrieve User ID based on email_id
"""
def get_owner_id_from_email_id(mail_id: int) -> int:
    return db.session.query(EmailAddress) \
            .filter(EmailAddress.email_id == mail_id) \
            .first() \
            .get_owner_id()

"""
Function to check if detected mail item is not already in the database
Returns a boolean as result
This is to avoid duplicate rows of same item by
same receiver, same subject, sa me content.
If a user clicks on check multiple times in same day the detection
will continue to detect mails received after last_updated (inclusive of same day)
resulting in duplicate rows added to DB, so this is to mitigate that
"""
def check_p_mail_exist(email_id: int, subject: str, content: str) -> bool:
    result = db.session.query(PhishingEmail).filter( \
    PhishingEmail.receiver_id == email_id,\
    PhishingEmail.subject == subject,\
    PhishingEmail.content == content).first()
    return True if result else False

"""
Function to remove reset_tokens in all User
Triggered as an hourly task via Flask-APScheduler
"""
def purge_user_tokens() -> None:
    logger.info("Routine task: purging all user tokens..")
    users = db.session.query(User).filter(User.reset_token != None).all()
    if users:
        for user in users:
            user.delete_reset_token()
    db.session.commit()

"""
Function to iterate through all active mailboxes to check for phishing emails
Triggered as a scheduled task via Flask-APScheduler
"""
def check_all_mailboxes() -> None:
    logger.info("Routine task: checking all active mailboxes..")

    all_active_mailboxes = db.session.query(EmailAddress)\
    .filter(EmailAddress.active == True)\
    .all()

    if all_active_mailboxes:
        logger.info("Checking through all active mailboxes")
        for mailaddr in all_active_mailboxes:
            try:
                imap_svr = get_imap_svr(mailaddr.get_email_address())

                logger.info("Email: %s -- IMAP: %s"\
                , mailaddr.get_email_address(), imap_svr)

                mailbox = MailBox(imap_svr)
                mailbox.login(mailaddr.get_email_address()\
                , mailaddr.get_decrypted_email_password())

                logger.info("Successfully logged in via IMAP")
            except ConnectionRefusedError:
                logger.error("Unable to connect to mailbox for %s"\
                , mailaddr.get_email_address())
                continue

            last_updated = mailaddr.get_last_updated().date()\
             if mailaddr.get_last_updated() else datetime.now().date()

            mailaddr.set_last_updated(datetime.now())

            logger.info("Updating mailbox last updated from %s to %s",\
             last_updated.strftime("%d-%m-%Y"), datetime.now())

            mailbox.folder.set("INBOX")
            logger.info("Fetching mails..")

            check_criteria = AND(date_gte=last_updated, seen=False)
            all_mails = mailbox.fetch(check_criteria, reverse=True\
            , mark_seen=False, bulk=True)

            logger.info("Mails fetched..")

            detection_count = 0

            for mail in all_mails:
                try:
                    sender = mail.from_
                except HeaderParseError:
                    logger.error("HeaderParseError, unparseable msg.from_."\
                    " Setting sender as INVALID_SENDER")
                    sender = 'INVALID_SENDER'

                if not sender == mailaddr.get_email_address() \
                or not sender == 'piscator.fisherman@gmail.com':
                    mail_item = EmailData(mail.subject, sender, mail.attachments\
                    , (mail.text + mail.html), mail.headers)
                    mail_item.generate_features()

                    result = model.predict(mail_item.repr_in_arr())
                    logger.info("Checking mail: %s -- Result: %s"\
                    , mail_item.get_subject(), result)

                    if result == 1:
                        logger.info("Phishing mail detected, subject: %s"\
                        , mail.subject)

                        mail_exist = check_p_mail_exist(mailaddr.get_email_id()\
                        , mail.subject, mail_item.get_content())

                        if not mail_exist:
                            detection_count +=1
                            detected_mail = PhishingEmail( \
                            sender_address = sender, \
                            subject = mail.subject, \
                            content = mail_item.get_content(), \
                            created_at = datetime.now(), \
                            receiver_id = mailaddr.get_email_id()
                            )
                            db.session.add(detected_mail)
            mailaddr.set_phishing_mail_detected(detection_count)
            logger.info("Finished checking mails.. logging out")
            mailbox.logout()
        db.session.commit()
