## Application objects
from app import db, logger, model

## Plugins
from flask_login import current_user

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
from sqlalchemy import Date, cast, func, extract

## Typehints
from typing import List, Dict

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
Function to retrieve active users, detection today and all time detection as a
Dictionary, meant for landing page statistics
"""
def get_homepage_stats() -> Dict:
    active_users = db.session.query(User).filter(User.is_active == True).count()
    detected_today = db.session.query(PhishingEmail)\
    .filter((cast(PhishingEmail.created_at, Date) == date.today())).count()
    all_time_detected = db.session.query(PhishingEmail).count()

    statistics = {
        'active_users' : active_users,
        'detected_today' : detected_today,
        'all_time_detected' : all_time_detected
    }

    return statistics

"""
Function to retrieve card and chart data for Administrator Dashboard as a
Dictionary. Does not include Monthly Overview chart
"""
def get_admin_dashboard_stats() -> Dict:
    # -- User statistics START
    all_users = db.session.query(User)
    users_active = all_users.filter(User.is_active==True).count()
    users_inactive = all_users.filter(User.is_active==False).count()
    user_stats = [users_inactive, users_active]
    # -- User statistics END

    # -- Email statistics START
    all_emails = db.session.query(EmailAddress)
    email_active = all_emails.filter(EmailAddress.active==True).count()
    email_inactive = all_emails.filter(EmailAddress.active==False).count()
    email_stats = [email_inactive, email_active]
    # -- Email statistics END

    # -- Phishing Emails Overview START
    all_time_detected = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id)

    today_detected = all_time_detected \
    .filter((cast(PhishingEmail.created_at, Date) == date.today()))

    weekly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_week == datetime.now().isocalendar()[1])

    # Likewise for month, same as week
    monthly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_month == datetime.now().month \
    , PhishingEmail.created_at_year == datetime.now().year)

    statistics = {
        'user_stats' : [users_active, users_inactive],
        'email_stats' : [email_active, email_inactive],
        'all_time' : all_time_detected.count(),
        'monthly' : monthly_detected.count(),
        'weekly' : weekly_detected.count(),
        'today' : today_detected.count()
    }
    return statistics

"""
Function to retrieve card and chart data for Subscriber Dashboard as a
Dictionary. Does not include Monthly Overview chart
"""
def get_user_dashboard_stats() -> Dict:
    # -- Email Address Status Count START
    all_emails = db.session.query(EmailAddress)\
    .filter(EmailAddress.owner_id==current_user.user_id)
    email_active = all_emails.filter(EmailAddress.active==True).count()
    email_inactive = all_emails.filter(EmailAddress.active==False).count()
    email_stats = all_emails.count()
    # -- Email Address Status count END

    # -- Phishing Emails Overview START
    all_time_detected = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
    , EmailAddress.owner_id==current_user.user_id)

    today_detected = all_time_detected \
    .filter((cast(PhishingEmail.created_at, Date) == date.today()))

    weekly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_week == datetime.now().isocalendar()[1])

    monthly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_month == datetime.now().month \
    , PhishingEmail.created_at_year == datetime.now().year)

    statistics = {
        'all_time' : all_time_detected.count(),
        'today' : today_detected.count(),
        'weekly' : weekly_detected.count(),
        'monthly' : monthly_detected.count(),
        'email_active' : email_active,
        'email_inactive' : email_inactive,
        'email_stats' : email_stats,
    }

    return statistics

"""
Function to retrieve monthly statistics for Subscriber Dashboard as a List.
"""
def get_user_monthly_overview() -> List:
    monthly_stats = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }

    month = func.date_trunc('month', func.cast(PhishingEmail.created_at, Date))

    # Returns a list of PE owned by cur_user's all email addresses that was detected
    # in the current year
    mails_detected_yearly = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
    , EmailAddress.owner_id==current_user.user_id \
    , PhishingEmail.created_at_year == datetime.now().year) \
    .order_by(month).all()

    for pe in mails_detected_yearly:
        monthly_stats[pe.get_created_month()] = monthly_stats\
        .get(pe.get_created_month(), 0)+1
    monthly_stats = list(monthly_stats.values())
    # -- Phishing Emails Overview END

    return monthly_stats

"""
Function to retrieve monthly statistics for Administrator Dashboard as a List
"""
def get_admin_monthly_overview() -> List:
    monthly_stats = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }

    month = func.date_trunc('month', func.cast(PhishingEmail.created_at, Date))

    # Returns a list of PE in all email addresses that was detected
    # in the current year
    mails_detected_yearly = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
    , PhishingEmail.created_at_year == datetime.now().year) \
    .order_by(month).all()

    for pe in mails_detected_yearly:
        monthly_stats[pe.get_created_month()] = monthly_stats\
        .get(pe.get_created_month(), 0)+1
    monthly_stats = list(monthly_stats.values())
    return monthly_stats

"""
Function to disable email addresses owned by a User by ID.
"""
def disable_emails_by_user_id(id) -> None:
    user_emails = get_existing_addresses_by_user_id(id)
    for email in user_emails:
        logger.info("Disabling %s", email)
        email.set_active_status(False)

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
            mail_check_count = 0

            for mail in all_mails:
                try:
                    sender = mail.from_
                except HeaderParseError:
                    logger.error("HeaderParseError, unparseable msg.from_."\
                    " Setting sender as INVALID_SENDER")
                    sender = 'INVALID_SENDER'

                if not sender == mailaddr.get_email_address() \
                or not sender == 'piscator.fisherman@gmail.com':

                    mail_check_count+=1

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
            mailaddr.set_total_mails_checked(mail_check_count)
            logger.info("Finished checking mails.. logging out")
            mailbox.logout()
        db.session.commit()

"""
Function to delete all inactive email addresses
Triggered as a scheduled task via Flask-APScheduler
"""
def delete_inactive_emails() -> None:
    all_inactive_mailboxes = db.session.query(EmailAddress)\
    .filter(EmailAddress.active == False)\
    .all()

    for email in all_inactive_mailboxes:
        db.session.delete(email)

    db.session.commit()

"""
Function to delete all inactive subscriber accounts
Triggered as a scheduled task via Flask-APScheduler
"""
def delete_inactive_accounts() -> None:
    all_inactive_accounts = db.session.query(User)\
    .filter(User.is_active == False)\
    .all()

    for account in all_inactive_accounts:
        db.session.delete(user)

    db.session.commit()
