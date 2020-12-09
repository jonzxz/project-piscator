from app import app, db, logger

## Plugins
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for, session

## Forms
from app.forms.RegistrationForm import RegistrationForm
from app.forms.LoginForm import LoginForm
from app.forms.AddEmailForm import AddEmailForm
from app.forms.ContactForm import ContactForm
from app.forms.AccountSettingsForm import AccountSettingsForm

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Datetime
from datetime import datetime

## Utils
from app.utils.EmailUtils import test_mailbox_conn
from app.utils.EmailUtils import send_contact_us_email
from app.utils.EmailUtils import get_imap_svr

## Exceptions
from sqlalchemy.exc import IntegrityError

# Mailbox
from imap_tools import MailBox
from app.models.Mail import Mail


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    contact_form = ContactForm()
    if request.method == 'POST':
        logger.debug("Email received")
        send_contact_us_email(contact_form.email_address.data, contact_form.message.data)
        return redirect(url_for('contact_form_reset'))
    return render_template('index.html', contact_form = contact_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug("Entering register function")
    if current_user.is_authenticated:
        logger.info("User is logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if request.method =='POST':
        logger.debug("Register form submitted")
        if form.validate_on_submit():
            user_exist = db.session.query(User).filter(User.username == form.username.data).first()
            if user_exist == None:
                new_user = User(username=form.username.data)
                new_user.set_password(form.password.data)
                new_user.set_last_logged_in(datetime.now())
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session["user_id"] = new_user.get_id()
                session["username"] = new_user.get_username()
                logger.debug("Successfully created user %s", new_user)
                return redirect(url_for('dashboard'))
            else:
                flash("Username already taken!")
                logger.error("Username already taken")
                logger.warning("Registration failed, user not registered")
                return redirect(url_for("reg_form_reset"))
                # return render_template('success.html', usrname = form.username.data

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    logger.debug("Entering login function")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        user.set_last_logged_in(datetime.now())
        db.session.commit()
        session["user_id"] = user.get_id()
        session["username"] = user.get_username()
        logger.debug("Successfully logged in user %s", user)
        if user.is_admin:
            return redirect(url_for('admin'))
        if not user.is_admin:
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    session.pop('username', None)
    logger.debug("Successfully logged out")
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin/index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    logger.info("Entering dashboard home..")
    if current_user.is_anonymous:
        logger.warning("Anonymous user in dashboard home, going to index..")
        return redirect(url_for('index'))
    return render_template('dashboard/dashboard_home.html')

@app.route('/dashboard/emails', methods=['GET', 'POST'])
def dash_email():
    logger.info("Entering dashboard emails..")
    # Redirects non-logged in users to index if they access dashboard from URL
    if current_user.is_anonymous:
        logger.warning("User is anonymous, redirecting to index")
        return redirect(url_for('index'))
    form = AddEmailForm()

    ## --- Add Email Form submission START ---
    if form.validate_on_submit():
        email_addr = form.email_address.data
        password = form.password.data

        # Checks if email already exist in database
        email_exist = db.session.query(EmailAddress).filter(EmailAddress.email_address == email_addr).first()

        if email_exist == None:
            # Attempts a mailbox login via imap_tools based on submit
            # Adds the email address to the database
            logger.info("Checking mailbox connectivity..")
            # -- If you want to test adding emails to a user account without checking connection
            # -- change the if statement to if True:
            # if test_mailbox_conn(email_addr, password):
            if True:
                new_email = EmailAddress()
                new_email.set_email_address(form.email_address.data)
                new_email.set_email_password(form.password.data)
                new_email.set_user_id(current_user.user_id)
                new_email.set_created_at(datetime.now())
                new_email.set_active_status(True)
                db.session.add(new_email)
                db.session.commit()
            # If connection to mailbox fails
            else:
                flash("Unable to connect to mailbox.")
        else:
            flash("{} already exist in our database!".format(email_addr))
            logger.error("Email already exist")
            return redirect(url_for('mail_form_reset'))
    ## -- Add Email Form submission END --

    ## -- Default Dashboard Loading START --
    existing_emails = db.session.query(EmailAddress).filter(EmailAddress.user_id == current_user.user_id).all()
    logger.debug(existing_emails)
    return render_template('dashboard/dashboard_emails.html',
    current_user = current_user.username, form = form,
    user_emails = existing_emails)
    ## -- Default Dashboard Loading END --

@app.route('/dashboard/account', methods=['GET', 'POST'])
def dash_account():
    logger.info("Entering dashboard account..")
    if current_user.is_anonymous:
        logger.warning("Anonymous user in dashboard account, going to index..")
        return redirect(url_for('index'))

    form = AccountSettingsForm()

    if form.validate_on_submit():
        logger.debug("%s password change entered", user)
        user = db.session.query(User).filter(User.user_id == current_user.user_id).first()
        user.set_password(form.new_password.data)
        try:
            db.session.commit()
            logger.debug("Successfully changed user %s password, updated database", user)
        except IntegrityError:
            db.session.rollback()
            logger.error("Failed to change password for %s, rolling back database", user)

    return render_template('dashboard/dashboard_account.html',
    current_user = current_user.username, form = form)



@app.route('/dashboard/emails/phish/<mid>')
def check_phish(mid):
    mail_items = []

    logger.info("Click-to-check entered..")
    mailaddr = EmailAddress.query.filter_by(email_id=mid).first()
    mailaddr.set_last_updated(datetime.now())
    db.session.commit()
    logger.info("Mailbox selected is %s", mailaddr.get_email_address())

    imap_svr = get_imap_svr(mailaddr.get_email_address())
    logger.info("Retrieving IMAP server: %s", imap_svr)
    mailbox = MailBox(imap_svr)
    mailbox.login(mailaddr.get_email_address(), mailaddr.get_decrypted_email_password())
    mailbox.folder.set("INBOX")
    logger.info("Connected to mailbox %s", mailaddr.get_email_address())
    logger.info("Fetching mails..")

    all_mails = mailbox.fetch(reverse=True, mark_seen=False, bulk=True)
    logger.info("Mails fetched..")

    for msg in all_mails:
        if not msg.from_ == mailaddr.get_email_address():
            logger.info("Date: {}".format(msg.date))
            logger.info("Sender: {}".format(msg.from_))
            logger.info("Subject: {}".format(msg.subject))
            mail_items.append(Mail(msg.from_, msg.date, msg.subject))

    logger.info("Finished displaying all mails.. logging out")
    mailbox.logout()

    # return redirect(url_for('dashboard'))
    return render_template('success.html', mail_items = mail_items)

@app.route('/dashboard/emails/activation/<mid>')
def mail_activation(mid):
    logger.info("Entering function to enable/disable email..")
    mailaddr = EmailAddress.query.filter_by(email_id=mid).first()
    if mailaddr.get_active_status() == True:
        mailaddr.set_active_status(False)
    else:
        mailaddr.set_active_status(True)
    db.session.commit()
    return redirect(url_for('dash_email'))

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def tos():
    return render_template('privacy.html')

# Reroute functions to prevent form resubmission on refresh
@app.route('/mail_form_reset', methods=['GET'])
def mail_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('dash_email'))

@app.route('/reg_form_reset', methods=['GET'])
def reg_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('register'))

@app.route('/contact_form_reset', methods=['GET'])
def contact_form_reset():
    return redirect(url_for('index'))
